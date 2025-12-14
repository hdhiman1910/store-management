from flask import request, jsonify
from flask_restful import Resource, marshal_with, fields
from services import ProductService

section_fields = {
    'name': fields.String,
}

marshal_fields = {
    'name': fields.String,
    'price': fields.Float,
    'stock': fields.Integer,
    'expiry': fields.DateTime,
    'mfd': fields.DateTime,
    'unit_of_measure': fields.String,
    'description': fields.String,
    'section': fields.Nested(section_fields),
}


class ProductResource(Resource):
    @marshal_with(marshal_fields)
    def get(self, id):
        item = ProductService.get_by_id(id)
        return item

class ProductListResource(Resource):
    @marshal_with(marshal_fields)
    def get(self):
        items = ProductService.get_all()
        return [item for item in items]