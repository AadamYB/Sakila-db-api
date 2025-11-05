from flask import Blueprint

from api.routes.actor import actors_router
from api.routes.film import films_router
from api.routes.language import languages_router
from api.routes.category import categories_router

routes = Blueprint('api', __name__, url_prefix='/api')

routes.register_blueprint(actors_router)
routes.register_blueprint(films_router)
routes.register_blueprint(languages_router)
routes.register_blueprint(categories_router)