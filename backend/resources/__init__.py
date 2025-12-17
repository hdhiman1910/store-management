from flask_restful import Api
from flask import Blueprint

from .auth_resource import auth_bp
from .products_resource import ProductResource, ProductListResource
from .section_resource import SectionResource, SectionListResource
from .user_resource import UserResource, UserListResource, approve_user

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(ProductResource, "/products/<int:id>")
api.add_resource(ProductListResource, "/products")

api.add_resource(SectionResource, "/sections/<int:id>")
api.add_resource(SectionListResource, "/sections")

api.add_resource(UserResource, "/users/<int:id>")
api.add_resource(UserListResource, "/users")

api_bp.add_url_rule("/users/approve/<int:id>", view_func=approve_user, methods=["POST"])