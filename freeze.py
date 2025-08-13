from __future__ import annotations

import shutil
from pathlib import Path

from flask_frozen import Freezer

from app import create_app


BUILD_DIR = "build"
STATIC_SRC = Path("portfolio") / "static"
STATIC_DEST = Path(BUILD_DIR) / "portfolio-static"


def main() -> None:
    app = create_app()
    freezer = Freezer(app)

    # Rutas a congelar de forma explícita (con barra final para generar index.html)
    @freezer.register_generator
    def static_pages():
        for path in ["/", "/proyectos/", "/diplomas/", "/sobre-mi/"]:
            yield path

    # Genera HTMLs
    freezer.freeze()

    # Copia estáticos a la carpeta de publicación con el mismo static_url_path
    shutil.rmtree(STATIC_DEST, ignore_errors=True)
    shutil.copytree(STATIC_SRC, STATIC_DEST)


if __name__ == "__main__":
    main()
