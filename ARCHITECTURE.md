# Arquitectura del proyecto

Este proyecto es un sitio personal (portafolio) construido con Flask siguiendo el patrón MVT (Model–View–Template). Incluye:
- Inicio con perfil, enlaces sociales con iconos, slider de tecnologías y proyectos destacados.
- Sección de diplomas con previsualización de PDFs integrada.
- Páginas de proyectos y sobre mí.

## Visión general
- Framework: Flask 3.x
- Patrón: MVT
- App factory: `create_app()` en `app.py`
- UI: Bootstrap 5 + estilos propios en `portfolio/static/css/styles.css`
- Assets: servidos desde el blueprint en `/portfolio-static/...`

## Estructura de carpetas
```
.
├─ app.py
├─ requirements.txt
├─ ARCHITECTURE.md
├─ README.md
└─ portfolio/
   ├─ __init__.py        # blueprint y registro
   ├─ models.py          # dataclasses y datos mock
   ├─ views.py           # rutas y composición de contexto
   ├─ templates/
   │  ├─ base.html
   │  ├─ index.html
   │  ├─ projects.html
   │  ├─ diplomas.html
   │  └─ about.html
   └─ static/
      ├─ css/styles.css
      ├─ images/perfil.jpg
      ├─ icons/linkedin.svg
      └─ Diplomas/*.pdf
```

## Componentes
- `app.py`
  - `create_app()`: crea la app, configura `SECRET_KEY`, registra el blueprint `portfolio` y añade un `context_processor` para `current_year`. Desactiva `static_folder` por defecto para evitar colisiones con el blueprint de estáticos.
- `portfolio/__init__.py`
  - Define `bp = Blueprint('portfolio', __name__, template_folder='templates', static_folder='static', static_url_path='/portfolio-static')`.
- `portfolio/models.py`
  - `Profile`, `Technology`, `Project` (dataclasses).
  - `get_sample_profile()`, `get_sample_stack()`, `get_sample_projects()` devuelven datos de ejemplo.
  - `Technology.category` permite ordenar el slider en una sola línea por categorías.
- `portfolio/views.py`
  - `index`: muestra perfil, slider ordenado y proyectos destacados (con “Repositorio” y “Ver sitio”).
  - `projects`: grilla de proyectos.
  - `about`: perfil extendido.
  - `diplomas`: lista PDFs desde `static/Diplomas`, prioriza el universitario y organiza el resto en grupos (medios y pequeños).
- `portfolio/templates/*`
  - `base.html`: navbar clara, footer y carga de estilos.
  - `index.html`: hero con avatar circular (borde luminoso), iconos de redes y slider infinito de tecnologías.
  - `diplomas.html`: previsualizadores embebidos con iframes sin toolbar.
- `styles.css`
  - Paleta clara y tipografía Inter; tarjetas con sombras suaves; animación sutil del borde del avatar; slider infinito con pausa al hover; estilos de previews PDF.

## Flujos
- Inicio `/`: ordena tecnologías por categorías (Lenguajes → Bases de datos → Desarrollo → Infraestructura) y renderiza en una sola línea con animación.
- Diplomas `/diplomas`: detecta el diploma universitario (`1825-AA-*`) y lo destaca; los demás se muestran en tamaños medio/pequeño.
- Proyectos `/proyectos`: lista y enlaces a repos y sitios.

## Decisiones
- `static_url_path` propio para el blueprint: evita conflicto con `Flask(static_folder)`.
- Ícono LinkedIn local por confiabilidad; otros iconos desde CDN o también se pueden servir localmente.
- Datos mock en `models.py` pensados para evolucionar a BD/JSON.

## Extensiones futuras
- Persistencia: JSON/SQLite + capa de repositorios.
- Blog: modelos y vistas para posts.
- Formulario de contacto con `Flask-WTF` y proveedor de correo.
- i18n con `Flask-Babel`.
- Tests con `pytest`.

## Despliegue (sugerido)
- WSGI (Gunicorn) detrás de Nginx o plataforma PaaS.
- Variables: `SECRET_KEY` estable y `FLASK_ENV=production`.
- Cache/CDN para estáticos (`/portfolio-static`).
