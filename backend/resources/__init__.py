from flask_restful import Api
from flask import Blueprint

from .auth_resource import auth_bp
from .products_resource import ProductResource, ProductListResource

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(ProductResource, "/products/<int:id>")
api.add_resource(ProductListResource, "/products")