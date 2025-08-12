from flask import Flask
from datetime import datetime


def create_app() -> Flask:
    # Desactiva el static por defecto para evitar colisión con blueprint
    app = Flask(__name__, static_folder=None)
    app.config["SECRET_KEY"] = "dev"

    # Registro del blueprint principal del portafolio
    from portfolio import bp as portfolio_bp
    app.register_blueprint(portfolio_bp)

    # Context processor para variables globales en templates
    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.now().year,
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)