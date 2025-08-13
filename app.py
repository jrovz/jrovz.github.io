from flask import Flask, request
from datetime import datetime
from flask_babel import Babel, _


def create_app() -> Flask:
    # Desactiva el static por defecto para evitar colisión con blueprint
    app = Flask(__name__, static_folder=None)
    app.config["SECRET_KEY"] = "dev"
    app.config["BABEL_DEFAULT_LOCALE"] = "es"
    app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"

    # Registro del blueprint principal del portafolio
    from portfolio import bp as portfolio_bp
    app.register_blueprint(portfolio_bp)

    # i18n: inicializa Babel con selector de locale según prefijo de URL
    def select_locale() -> str:
        path = request.path or "/"
        return "en" if path.startswith("/en/") or path == "/en/" else "es"

    Babel(app, locale_selector=select_locale)

    # Context processor para variables globales en templates
    @app.context_processor
    def inject_globals():
        path = request.path or "/"
        lang = "en" if path.startswith("/en/") or path == "/en/" else "es"

        # Calcula URL alterna para switch ES/EN
        if lang == "es":
            if path == "/":
                alt = "/en/"
            else:
                alt = (
                    path
                    .replace("/proyectos/", "/en/projects/")
                    .replace("/diplomas/", "/en/diplomas/")
                    .replace("/sobre-mi/", "/en/about/")
                )
        else:
            if path == "/en/":
                alt = "/"
            else:
                alt = (
                    path
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