from flask import Flask, request
from datetime import datetime
from flask_babel import Babel, _


def create_app() -> Flask:
    # Desactiva el static por defecto para evitar colisión con blueprint
    app = Flask(__name__, static_folder=None)
    app.config["SECRET_KEY"] = "dev"
    app.config["BABEL_DEFAULT_LOCALE"] = "es"
    app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
    app.config["BABEL_SUPPORTED_LOCALES"] = ["es", "en"]

    # Registro del blueprint principal del portafolio
    from portfolio import bp as portfolio_bp
    app.register_blueprint(portfolio_bp)

    # i18n: inicializa Babel con selector de locale según prefijo de URL
    def select_locale() -> str:
        # Fallback global locale; vistas fuerzan locale por ruta con force_locale
        path = (request.path or "/").strip("/")
        first_segment = path.split("/", 1)[0] if path else ""
        return "en" if first_segment == "en" else "es"

    Babel(app, locale_selector=select_locale)

    # Context processor para variables globales en templates
    @app.context_processor
    def inject_globals():
        raw_path = request.path or "/"
        norm = raw_path if raw_path.endswith("/") else f"{raw_path}/"
        first_segment = raw_path.strip("/").split("/", 1)[0] if raw_path != "/" else ""
        lang = "en" if first_segment == "en" else "es"

        # Calcula URL alterna para switch ES/EN
        if lang == "es":
            if norm == "/":
                alt = "/en/"
            else:
                alt = (
                    norm
                    .replace("/proyectos/", "/en/projects/")
                    .replace("/diplomas/", "/en/diplomas/")
                    .replace("/sobre-mi/", "/en/about/")
                )
        else:
            if norm == "/en/":
                alt = "/"
            else:
                alt = (
                    norm
                    .replace("/en/projects/", "/proyectos/")
                    .replace("/en/diplomas/", "/diplomas/")
                    .replace("/en/about/", "/sobre-mi/")
                )

        return {
            "current_year": datetime.now().year,
            "lang": lang,
            "alt_lang_url": alt,
            "_": _,
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)