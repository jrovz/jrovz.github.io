from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.public import bp
from app.models.producto import Producto
from app.models.cliente import Cliente, Mensaje, Cita
from app.models.servicio import Servicio # Asegúrate de que este modelo existe
from app.models.barbero import Barbero, DisponibilidadBarbero
from app.models.categoria import Categoria # <<< IMPORT Categoria MODEL
try:
    from app.models.slider import Slider
except Exception as e:
    print(f"Warning: No se pudo importar el modelo Slider: {e}")
    Slider = None
from app.models.email import send_appointment_confirmation_email # Importar la función de envío
from app import db
from datetime import datetime, timedelta, time

@bp.route('/')
def home():
    # Inicializar todas las variables al principio para evitar errores
    featured_products = []
    barberos = []
    servicios = []
    fechas_disponibles = []
    sliders = []
    
    try:
        # Obtener sliders activos ordenados por orden
        if Slider is not None:
            sliders = Slider.get_active_slides_ordered()
        else:
            print("Warning: Modelo Slider no disponible, usando lista vacía")
            sliders = []
        
        # Productos destacados
        # CORREGIDO: Usar 'creado' en lugar de 'created_at'
        featured_products = Producto.query.order_by(Producto.creado.desc()).limit(3).all() 
        
        # --- START REFINED DEBUG ---
        print("--- DEBUG: Querying ALL Barberos ---")
        all_barberos = Barbero.query.all()
        print(f"Total barberos found (before filter): {len(all_barberos)}")
        for b in all_barberos:
            # Imprimir valor y tipo del campo activo
            print(f"  ID: {b.id}, Nombre: {b.nombre}, Activo (DB value): {b.activo}, Type: {type(b.activo)}")
            
        print("--- DEBUG: Querying ACTIVE Barberos ---")
        barberos = Barbero.query.filter_by(activo=True).all()
        print(f"Barberos found with filter_by(activo=True): {len(barberos)}")
        for b in barberos:
            print(f"  Active Barbero ID: {b.id}, Nombre: {b.nombre}")

        print("--- DEBUG: Querying ALL Servicios ---")
        all_servicios = Servicio.query.all()
        print(f"Total servicios found (before filter): {len(all_servicios)}")
        for s in all_servicios:
             # Imprimir valor y tipo del campo activo
             print(f"  ID: {s.id}, Nombre: {s.nombre}, Activo (DB value): {s.activo}, Type: {type(s.activo)}")

        print("--- DEBUG: Querying ACTIVE Servicios ---")
        servicios = Servicio.query.filter_by(activo=True).order_by(Servicio.orden.asc(), Servicio.nombre.asc()).all()
        print(f"Servicios found with filter_by(activo=True): {len(servicios)}")
        for s in servicios:
            print(f"  Active Servicio ID: {s.id}, Nombre: {s.nombre}")
        # --- END REFINED DEBUG ---
        
        # Generar fechas para el calendario
        hoy = datetime.now().date()
        fechas_disponibles = [hoy + timedelta(days=i) for i in range(14)]
        
    except Exception as e:
        print(f"Error in home(): {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Final check before rendering
    print(f"--- FINAL CHECK before render ---")
    print(f"Barberos to template: {len(barberos)}")
    print(f"Servicios to template: {len(servicios)}")
    
    # Eliminar los prints de depuración anteriores si aún existen
    # print(f"Enviando a template: {len(barberos)} barberos, {len(servicios)} servicios")
    # print("--- DEBUG HOME ---")
    # ... (eliminar bucles for anteriores) ...
    # print("--- FIN DEBUG HOME ---")

    return render_template('public/Home.html',
                          featured_products=featured_products,
                          barberos=barberos,
                          servicios=servicios,
                          fechas_disponibles=fechas_disponibles,
                          sliders=sliders)

@bp.route('/about')
def about():
    return render_template("about.html")

@bp.route('/contacto', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Guardar mensaje en la base de datos
        nuevo_cliente = Cliente(
            nombre=request.form.get('nombre'),
            email=request.form.get('email'),
            telefono=request.form.get('telefono')
        )
        
        db.session.add(nuevo_cliente)
        db.session.flush()  # Para obtener el ID antes del commit final
        
        nuevo_mensaje = Mensaje(
            cliente_id=nuevo_cliente.id,
            asunto=request.form.get('asunto'),
            mensaje=request.form.get('mensaje')
        )
        
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        return 'Formulario enviado correctamente', 201
    return render_template("contacto.html")

@bp.route('/productos')
def productos():
    """Página de productos agrupados por categoría."""
    
    categorias_con_productos = [] # Nueva estructura para pasar a la plantilla

    try:
        # Obtener todas las categorías ordenadas por nombre
        todas_categorias = Categoria.query.order_by(Categoria.nombre).all()
        
        for categoria in todas_categorias:
            # Obtener productos activos para esta categoría
            # Asumiendo que Producto tiene una relación llamada 'categoria_rel' y un campo 'activo'
            productos_activos = Producto.query.filter_by(
                categoria_id=categoria.id, 
                activo=True
            ).order_by(Producto.nombre).all()
            
            # Si la categoría tiene productos activos, añadirla a la lista
            if productos_activos:
                categorias_con_productos.append({
                    'categoria': categoria, # Pasamos el objeto categoría completo
                    'productos': productos_activos
                })
                
    except Exception as e:
        flash(f"Error al cargar productos: {str(e)}", "danger")
        # Log the error for debugging
        current_app.logger.error(f"Error in /productos route: {e}")

    return render_template(
        'public/productos.html',
        categorias_con_productos=categorias_con_productos # Pasamos la nueva estructura
    )

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    from app.public.forms import CheckoutForm
    from app.models.pedido import Pedido, PedidoItem
    from app.models.producto import Producto
    import json
    
    form = CheckoutForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Obtener datos del carrito desde el formulario
                cart_data = request.form.get('cart_data')
                if not cart_data:
                    flash('El carrito está vacío', 'error')
                    return redirect(url_for('public.checkout'))
                
                cart_items = json.loads(cart_data)
                
                if not cart_items:
                    flash('El carrito está vacío', 'error')
                    return redirect(url_for('public.checkout'))
                
                # Crear el pedido
                nuevo_pedido = Pedido(
                    numero_pedido=f"PED{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    cliente_nombre=form.nombre.data,
                    cliente_email=form.email.data,
                    cliente_telefono=form.telefono.data,
                    notas=form.notas.data,
                    total=0  # Se calculará después
                )
                
                db.session.add(nuevo_pedido)
                db.session.flush()  # Para obtener el ID
                
                # Procesar items del carrito
                total_pedido = 0
                for item in cart_items:
                    producto = Producto.query.get(item['id'])
                    if producto:
                        cantidad = int(item['quantity'])
                        subtotal = float(producto.precio) * cantidad
                        
                        pedido_item = PedidoItem(
                            pedido_id=nuevo_pedido.id,
                            producto_id=producto.id,
                            producto_nombre=producto.nombre,
                            producto_precio=producto.precio,
                            cantidad=cantidad,
                            subtotal=subtotal
                        )
                        
                        db.session.add(pedido_item)
                        total_pedido += subtotal
                
                # Actualizar el total del pedido
                nuevo_pedido.total = total_pedido
                db.session.commit()
                
                flash('¡Pedido creado exitosamente!', 'success')
                return redirect(url_for('public.confirmacion_pedido', pedido_id=nuevo_pedido.id))
                
            except Exception as e:
                db.session.rollback()
                flash('Error al procesar el pedido. Intenta de nuevo.', 'error')
                print(f"Error en checkout: {e}")
    
    return render_template('public/checkout.html', form=form)

@bp.route('/confirmacion-pedido/<int:pedido_id>')
def confirmacion_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('public/confirmacion_pedido.html', pedido=pedido)

@bp.route('/servicios')
def servicios():
    try:
        # Inicializar servicios con una lista vacía por si acaso falla
        servicios_activos = []
        
        # Intentar verificar la conexión a la base de datos primero
        from sqlalchemy.sql import text
        from app import db
        db.session.execute(text("SELECT 1"))
        print("Conexión a la base de datos verificada correctamente")
        
        # Obtener solo los servicios marcados como activos
        print("Consultando servicios activos...")
        servicios_activos = Servicio.query.filter_by(activo=True).order_by(Servicio.nombre).all()
        print(f"Servicios encontrados: {len(servicios_activos)}")
        
        return render_template("public/servicios.html", 
                            servicios=servicios_activos)
    except Exception as e:
        print(f"Error al consultar servicios: {str(e)}")
        import traceback
        traceback.print_exc()
        # Devolver una lista vacía en caso de error para no romper la página
        return render_template("public/servicios.html", 
                            servicios=[], error_msg=f"No se pudieron cargar los servicios: {str(e)}")

@bp.route('/api/servicio/<int:servicio_id>')
def get_servicio_data(servicio_id):
    """API endpoint para obtener datos de un servicio específico"""
    try:
        servicio = Servicio.query.filter_by(id=servicio_id, activo=True).first()
        if not servicio:
            return jsonify({'error': 'Servicio no encontrado'}), 404
        
        # Formatear el precio usando la función format_cop
        from app.utils import format_cop
        
        # Obtener todas las imágenes del servicio
        imagenes_galeria = servicio.get_imagenes_activas()
        imagenes_urls = [img.ruta_imagen for img in imagenes_galeria] if imagenes_galeria else []
        
        # Si no hay imágenes en la galería, usar imagen_url como fallback
        if not imagenes_urls and servicio.imagen_url:
            imagenes_urls = [servicio.imagen_url]
        
        servicio_data = {
            'id': servicio.id,
            'nombre': servicio.nombre,
            'descripcion': servicio.descripcion or 'Sin descripción disponible',
            'precio_formateado': format_cop(servicio.precio),
            'precio_valor': float(servicio.precio),
            'duracion_estimada': servicio.duracion_estimada,
            'imagen_url': servicio.get_imagen_principal(),  # Imagen principal para compatibilidad
            'imagenes': imagenes_urls,  # Array de todas las imágenes
            'total_imagenes': len(imagenes_urls),
            'activo': servicio.activo
        }
        
        return jsonify(servicio_data)
        
    except Exception as e:
        current_app.logger.error(f"Error al obtener datos del servicio {servicio_id}: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# @bp.route('/barberos/<int:id>/disponibilidad', methods=['GET', 'POST'])
# @login_required
# def gestionar_disponibilidad(id):
#     if not current_user.is_admin():
#         abort(403)
    
#     barbero = Barbero.query.get_or_404(id)
#     form = DisponibilidadForm()
    
#     if form.validate_on_submit():
#         # Convertir strings a objetos time
#         from datetime import datetime
#         hora_inicio = datetime.strptime(form.hora_inicio.data, '%H:%M').time()
#         hora_fin = datetime.strptime(form.hora_fin.data, '%H:%M').time()
        
#         disponibilidad = DisponibilidadBarbero(
#             barbero_id=barbero.id,
#             dia_semana=form.dia_semana.data,
#             hora_inicio=hora_inicio,
#             hora_fin=hora_fin,
#             activo=form.activo.data
#         )
        
#         db.session.add(disponibilidad)
#         try:
#             db.session.commit()
#             flash('Disponibilidad añadida correctamente', 'success')
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error al añadir disponibilidad: {str(e)}', 'danger')
            
#         return redirect(url_for('admin.gestionar_disponibilidad', id=barbero.id))
    
#     # Mostrar disponibilidad actual
#     disponibilidades = DisponibilidadBarbero.query.filter_by(barbero_id=barbero.id).order_by(DisponibilidadBarbero.dia_semana).all()
    
#     return render_template('admin/disponibilidad.html', 
#                            title=f'Disponibilidad de {barbero.nombre}',
#                            form=form,
#                            barbero=barbero,
#                            disponibilidades=disponibilidades)

@bp.route('/api/disponibilidad/<int:barbero_id>/<string:fecha>')
def disponibilidad_barbero(barbero_id, fecha):
    """
    Obtiene los horarios disponibles para un barbero en una fecha específica,
    considerando la duración de un servicio.

    Args:
        barbero_id (int): ID del barbero.
        fecha (str): Fecha en formato YYYY-MM-DD.

    Query Params:
        servicio_id (int): ID del servicio seleccionado.
    """
    try:
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
        barbero = Barbero.query.get_or_404(barbero_id)

        servicio_id = request.args.get('servicio_id', type=int)
        duracion_servicio = 30 

        if servicio_id:
            servicio = Servicio.query.get(servicio_id)
            if servicio:
                duracion_servicio = servicio.get_duracion_minutos()
                print(f"Servicio '{servicio.nombre}': {duracion_servicio} minutos")
            else:
                print(f"Warning: Servicio con ID {servicio_id} no encontrado. Usando duración por defecto.")
        else:
             print("Warning: No se proporcionó servicio_id. Usando duración por defecto.")

        horarios_obj_list = barbero.obtener_horarios_disponibles(fecha_dt, duracion_servicio)

        horarios_disponibles_str = []
        if horarios_obj_list:
            for slot in horarios_obj_list:
                if slot['disponible']:
                    horarios_disponibles_str.append(slot['hora'])
        
        mensaje_respuesta = f'Horarios disponibles para {barbero.nombre} el {fecha}'
        if not horarios_disponibles_str: # Comprobar la lista de strings filtrada
             disponibilidades_dia = barbero.get_disponibilidad_por_dia(fecha_dt.weekday())
             if not disponibilidades_dia:
                 mensaje_respuesta = f"{barbero.nombre} no tiene horario configurado para este día."
             else:
                 mensaje_respuesta = f"No hay horarios disponibles para {barbero.nombre} el {fecha} con duración de {duracion_servicio} min."


        return jsonify({
            'barbero': barbero.nombre,
            'fecha': fecha,
            'horarios': horarios_disponibles_str, # Usar la lista de strings de horas disponibles
            'mensaje': mensaje_respuesta 
        })

    except ValueError as ve:
         print(f"Error de formato en disponibilidad_barbero: {str(ve)}")
         return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD.'}), 400
    except Exception as e:
        print(f"Error en disponibilidad_barbero: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error interno al obtener disponibilidad.'}), 500

@bp.route('/api/agendar-cita', methods=['POST'])
def agendar_cita():
    try:
        data = request.json
        current_app.logger.info(f"Datos recibidos para agendar cita: {data}")

        required_fields = ['barbero_id', 'servicio_id', 'fecha', 'hora', 'nombre', 'email', 'telefono']
        for field in required_fields:
            if field not in data or not data[field]:
                current_app.logger.error(f"Campo faltante o vacío: {field}")
                return jsonify({'error': f'Falta el campo o está vacío: {field}'}), 400

        fecha_hora_str = f"{data['fecha']} {data['hora']}"
        fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')

        # Obtener la duración del servicio para verificar conflictos
        servicio = Servicio.query.get(int(data['servicio_id']))
        duracion_servicio = servicio.get_duracion_minutos() if servicio else 30
        
        # Calcular el rango de tiempo que ocupará la nueva cita
        inicio_nueva_cita = fecha_hora
        fin_nueva_cita = inicio_nueva_cita + timedelta(minutes=duracion_servicio)
        
        # Obtener todas las citas del barbero para el día seleccionado
        fecha_inicio_dia = datetime.combine(fecha_hora.date(), datetime.min.time())
        fecha_fin_dia = fecha_inicio_dia + timedelta(days=1)
        
        citas_del_dia = Cita.query.filter(
            Cita.barbero_id == int(data['barbero_id']),
            Cita.estado.in_(['confirmada', 'pendiente_confirmacion']),
            Cita.fecha >= fecha_inicio_dia,
            Cita.fecha < fecha_fin_dia
        ).all()

        # Verificar solapamientos en Python
        hay_solapamiento = False
        for cita_existente in citas_del_dia:
            inicio_existente = cita_existente.fecha
            fin_existente = inicio_existente + timedelta(minutes=cita_existente.duracion or 30)
            
            # Verificar si hay solapamiento: la nueva cita no debe empezar antes de que termine una existente
            # ni terminar después de que empiece otra existente
            if not (fin_nueva_cita <= inicio_existente or inicio_nueva_cita >= fin_existente):
                hay_solapamiento = True
                current_app.logger.warning(f"Solapamiento detectado con cita ID {cita_existente.id}: "
                                         f"Existente: {inicio_existente} - {fin_existente}, "
                                         f"Nueva: {inicio_nueva_cita} - {fin_nueva_cita}")
                break

        if hay_solapamiento:
            current_app.logger.warning(f"Intento de agendar cita con solapamiento: Barbero {data['barbero_id']} desde {fecha_hora} hasta {fin_nueva_cita}")
            return jsonify({'error': 'Este horario se solapa con otra cita. Por favor, selecciona otro horario.'}), 409 # 409 Conflict

        cliente = Cliente.query.filter_by(email=data['email']).first()
        if not cliente:
            cliente = Cliente(
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono']
            )
            db.session.add(cliente)
            db.session.flush() # Para obtener el ID del cliente si es nuevo
        else: # Actualizar datos si el cliente existe
            cliente.nombre = data['nombre']
            cliente.telefono = data['telefono']
            # No es necesario db.session.add(cliente) si ya existe y solo se modifica

        # Obtener la duración del servicio
        servicio = Servicio.query.get(int(data['servicio_id']))
        duracion_servicio = servicio.get_duracion_minutos() if servicio else 30
        
        nueva_cita = Cita(
            cliente_id=cliente.id,
            barbero_id=int(data['barbero_id']),
            servicio_id=int(data['servicio_id']),
            fecha=fecha_hora,
            estado='pendiente_confirmacion', # Estado inicial
            duracion=duracion_servicio,  # Guardar la duración del servicio
            notas=data.get('notas', '')
        )
        db.session.add(nueva_cita)
        db.session.commit() # Commit para obtener el ID de nueva_cita

        token = nueva_cita.generate_confirmation_token()
        current_app.logger.info(f"Cita ID {nueva_cita.id} creada, token generado. Enviando correo a {cliente.email}")

        # Enviar correo de confirmación
        # Las relaciones barbero y servicio_rel se cargarán automáticamente al acceder a ellas
        # en la plantilla del correo si no son lazy='dynamic' o si se accede a ellas antes.
        # Para estar seguros, podemos precargarlas o pasar los nombres directamente.
        # Aquí, el modelo Cita ya tiene las relaciones, así que deberían funcionar.

        send_appointment_confirmation_email(
            cliente_email=cliente.email,
            cliente_nombre=cliente.nombre,
            cita=nueva_cita, # Pasamos el objeto cita completo
            token=token
        )

        return jsonify({
            'success': True,
            'mensaje': 'Solicitud de cita recibida. Por favor, revisa tu correo electrónico para confirmar la cita en la próxima hora.',
            'cita_id': nueva_cita.id
        })

    except ValueError as ve:
        current_app.logger.error(f"Error de formato en agendar_cita: {str(ve)}")
        return jsonify({'error': f'Formato de fecha u hora inválido: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al agendar cita: {str(e)}", exc_info=True)
        return jsonify({'error': 'Ocurrió un error al procesar tu solicitud. Inténtalo de nuevo más tarde.'}), 500

@bp.route('/confirmar-cita/<token>', methods=['GET'])
def confirmar_cita_route(token):
    cita = Cita.verify_confirmation_token(token) # El método ya maneja la expiración
    
    if not cita:
        flash('El enlace de confirmación no es válido, ha expirado o la cita ya fue confirmada/cancelada.', 'danger')
        return render_template('public/confirmation_status.html',
                               success=False,
                               message='El enlace de confirmación no es válido, ha expirado o la cita ya no puede ser confirmada.')

    # Doble verificación de disponibilidad (opcional pero recomendado)
    # En caso de que otro usuario haya confirmado una cita para el mismo slot mientras este token estaba pendiente.
    conflicting_cita = Cita.query.filter(
        Cita.barbero_id == cita.barbero_id,
        Cita.fecha == cita.fecha,
        Cita.id != cita.id,
        Cita.estado == 'confirmada'
    ).first()

    if conflicting_cita:
        cita.estado = 'cancelada_conflicto' # O algún estado que indique esto
        db.session.commit()
        flash('Lo sentimos, este horario fue tomado justo antes de tu confirmación. Por favor, agenda de nuevo.', 'danger')
        return render_template('public/confirmation_status.html',
                               success=False,
                               message='Lo sentimos, este horario fue tomado justo antes de tu confirmación. Por favor, agenda de nuevo.')

    cita.estado = 'confirmada'
    cita.confirmed_at = datetime.utcnow()
    # El token ya no es necesario en la BD una vez usado si se genera bajo demanda.
    # Si lo estuvieras guardando, aquí lo invalidarías.
    db.session.commit()
    
    flash('¡Tu cita ha sido confirmada exitosamente!', 'success')
    # Opcional: Enviar notificación al barbero/admin.
    return render_template('public/confirmation_status.html',
                           success=True,
                           message='¡Tu cita ha sido confirmada exitosamente!',
                           cita=cita) # Pasar la cita para mostrar detalles