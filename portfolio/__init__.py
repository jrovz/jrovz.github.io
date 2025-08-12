from flask import Blueprint


# Blueprint principal del sitio de presentación personal
bp = Blueprint(
    "portfolio",
    __name__,
    template_folder="templates",
    static_folder="static",
    # Usar una ruta única para evitar conflicto con el /static del app principal
    static_url_path="/portfolio-static",
)


# Importa vistas para registrar las rutas en el blueprint
from . import views  # noqa: E402,F401


