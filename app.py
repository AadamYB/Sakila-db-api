from flask import Flask
from dotenv import load_dotenv
load_dotenv()

from api.config import Config, DevConfig, ProdConfig, get_config
from api.routes import routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    from api.models import db
    db.init_app(app)

    from api.schemas import ma
    ma.init_app(app)

    app.register_blueprint(routes)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()