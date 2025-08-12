# Portafolio personal (Flask)

Sitio web para presentación personal, stack tecnológico, proyectos y diplomas/certificaciones, construido con Flask siguiendo MVT.

## Requisitos
- Python 3.10+
- Windows/macOS/Linux

## Instalación rápida
```bash
# 1) Crear y activar entorno virtual (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Ejecutar
python app.py
# o
flask --app app run --debug
```

Abrir `http://127.0.0.1:5000`.

## Estructura
```text
.
├─ app.py
├─ requirements.txt
├─ ARCHITECTURE.md
├─ README.md
└─ portfolio/
   ├─ __init__.py
   ├─ models.py
   ├─ views.py
   ├─ templates/
   │  ├─ base.html
   │  ├─ index.html
   │  ├─ projects.html
   │  ├─ diplomas.html
   │  └─ about.html
   └─ static/
      ├─ css/styles.css
      ├─ images/perfil.jpg
      ├─ icons/
      │  └─ linkedin.svg
      └─ Diplomas/*.pdf
```

## Páginas
- `/` Inicio: hero con perfil y redes, slider de tecnologías, proyectos destacados.
- `/proyectos` Proyectos: grilla de proyectos.
- `/diplomas` Diplomas y certificaciones: previews embebidos de PDFs.
- `/sobre-mi` Sobre mí: perfil extendido.

## Configuración
- `portfolio/models.py`: editar `get_sample_profile()` (nombre, bio, enlaces reales) y `get_sample_projects()`.
- Para agregar más iconos sociales, usa `icon` con URL a SVG (o coloca el archivo en `portfolio/static/icons/` y referencia `icons/nombre.svg`).
- Para diplomas, añade PDFs a `portfolio/static/Diplomas/`.

## Despliegue
- Producción: WSGI server (Gunicorn) + Nginx o PaaS.
- Establecer `SECRET_KEY` seguro en `app.py` o por variable de entorno.

## Licencia
MIT.
