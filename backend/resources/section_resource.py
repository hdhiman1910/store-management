from flask import request, jsonify
from flask_restful import Resource, marshal, marshal_with, fields, reqparse
from services import SectionService as service, RequestService
from .resource_utils import validate_date
from .marshal_fields import section_fields as marshal_fields
from flask_security import current_user

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the section is required')

# api/sections/<int:id>
class SectionResource(Resource):
    @marshal_with(marshal_fields)
    def get(self, id):
        item = service.get_by_id(id)
        return item
    
    def put(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        # args = self.parser.parse_args()
        args = parser.parse_args()
        args['id'] = id

        if (current_user.has_role('manager')):
            RequestService.create({
                "data": args,
                "status": "created",
                "type": "section_update",
                "user_id": current_user.id
            })
            return {"message": "Update request created and sent for approval"}, 202



        item = service.update(args)
        return marshal(item, marshal_fields), 200
        # service.update(request.json)


    def patch(self, id):
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
        if (current_user.has_role('manager')):
            RequestService.create({
                "data": data,
                "status": "created",
                "type": "patch_section",
                "user_id": current_user.id
            })
            return {"message": "Update request created and sent for approval"}, 202
        item = service.update(data)
        return marshal(item, marshal_fields), 200

    def delete(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        
        if (current_user.has_role('manager')):
            RequestService.create({
                "data": {"id": id},
                "status": "created",
                "type": "delete_section",
                "user_id": current_user.id
            })
            return {"message": "Update request created and sent for approval"}, 202
        
        message = service.delete(id)
        return message, 200

# api/sections
class SectionListResource(Resource):
    @marshal_with(marshal_fields)
    def get(self):
        items = service.get_all()
        return (items)
    
    @marshal_with(marshal_fields)
    def post(self):
        args = parser.parse_args()

        if (current_user.has_role('manager')):
            RequestService.create({
                "data": args,
                "status": "created",
                "type": "post_section",
                "user_id": current_user.id
            })
            return {"message": "Update request created and sent for approval"}, 202
        
        item = service.create(args)
        return item, 201