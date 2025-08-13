from __future__ import annotations

import shutil
from pathlib import Path

from flask_frozen import Freezer
import subprocess

from app import create_app


BUILD_DIR = "build"
STATIC_SRC = Path("portfolio") / "static"
STATIC_DEST = Path(BUILD_DIR) / "portfolio-static"


def main() -> None:
    app = create_app()
    freezer = Freezer(app)

    # Rutas a congelar de forma explícita
    @freezer.register_generator
    def static_pages():
        # Usar barras finales para que genere .../index.html y Netlify sirva como text/html
        for path in [
            "/", "/proyectos/", "/diplomas/", "/sobre-mi/",
            "/en/", "/en/projects/", "/en/diplomas/", "/en/about/",
        ]:
            yield path

    # Compila traducciones (si existen) antes de congelar
    try:
        subprocess.run(["pybabel", "compile", "-d", "translations"], check=False)
    except Exception:
        pass

    # Genera HTMLs
    # Limpia el directorio de salida para evitar archivos obsoletos
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    freezer.freeze()

    # Copia estáticos a la carpeta de publicación con el mismo static_url_path
    shutil.rmtree(STATIC_DEST, ignore_errors=True)
    shutil.copytree(STATIC_SRC, STATIC_DEST)


if __name__ == "__main__":
    main()
