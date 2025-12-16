from flask import request, jsonify
from flask_restful import Resource, marshal, marshal_with, fields, reqparse
from services import UserService as service #
from .resource_utils import validate_date
from .marshal_fields import user_fields as marshal_fields #
from flask_security import current_user, roles_required, login_required

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the user is required')
parser.add_argument('email', type=str, required=True, help='Email of the user is required')

# api/users/<int:id>
class UserResource(Resource):
    # only admin can access user details
    @login_required
    def get(self, id):
        print(current_user.id)
        if (current_user.has_role('manager') or current_user.has_role('customer')) and current_user.id != id:
            return {"message": "ACCESS DENIED: You do not have permission to access other users' data"}, 403
        item = service.get_by_id(id)
        return marshal(item, marshal_fields)
    
    # only user himself or admin can update user details
    @login_required
    @marshal_with(marshal_fields)
    def put(self, id):
        if (current_user.has_role('manager') or current_user.has_role('customer')) and current_user.id != id:
            return {"message": "You do not have permission to update this user"}, 403
        item = service.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        args = parser.parse_args()
        args['id'] = id
        item = service.update(args)
        return item, 200

    @login_required
    @marshal_with(marshal_fields)
    def patch(self, id):
        if (current_user.has_role('manager') or current_user.has_role('customer')) and current_user.id != id:
            return {"message": "You do not have permission to update this user"}, 403

        item = service.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        data = request.get_json() or {}
        # validate/convert dates when provided in PATCH
        try:
            if 'expiry' in data and data['expiry'] is not None:
                data['expiry'] = validate_date(data['expiry'])
            if 'mfd' in data and data['mfd'] is not None:
                data['mfd'] = validate_date(data['mfd'])
        except ValueError as e:
            return {"message": str(e)}, 400

        data['id'] = id
        item = service.update(data)
        return item, 200

    @login_required
    def delete(self, id):
        if (current_user.has_role('manager') or current_user.has_role('customer')) and (current_user.id != id):
            return {"message": "You do not have permission to update this user"}, 403
        item = service.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        message = service.delete(id)
        return message, 200

# api/users
class UserListResource(Resource):
    # only admin should be to use this
    @roles_required('admin')
    @marshal_with(marshal_fields)
    def get(self):
        items = service.get_all()
        return (items)