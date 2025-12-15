from flask import request, jsonify
from flask_restful import Resource, marshal, marshal_with, fields, reqparse
from services import ProductService
from .resource_utils import validate_date

section_fields = {
    'name': fields.String,
}

marshal_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'stock': fields.Float,
    'expiry': fields.DateTime,
    'mfd': fields.DateTime,
    'unit_of_measure': fields.String,
    'section_id': fields.Integer,
    'description': fields.String,
    'section': fields.Nested(section_fields),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the product is required')
parser.add_argument('price', type=float, required=True, help='Price of the product is required')
parser.add_argument('stock', type=float, required=True, help='Stock of the product is required')
parser.add_argument('expiry', type=validate_date)
parser.add_argument('mfd', type=validate_date)
parser.add_argument('unit_of_measure', type=str, required=True, help='Unit of measure is required')
parser.add_argument('description', type=str)
parser.add_argument('section_id', type=int, required=True, help='Section ID is required check products_resource.py for more info')

# api/products/<int:id>
class ProductResource(Resource):
    @marshal_with(marshal_fields)
    def get(self, id):
        item = ProductService.get_by_id(id)
        return item
    
    @marshal_with(marshal_fields)
    def put(self, id):
        item = ProductService.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        # args = self.parser.parse_args()
        args = parser.parse_args()
        args['id'] = id
        item = ProductService.update(args)
        return item, 200
        # ProductService.update(request.json)

    @marshal_with(marshal_fields)
    def patch(self, id):
        item = ProductService.get_by_id(id)
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
        item = ProductService.update(data)
        return item, 200

    def delete(self, id):
        item = ProductService.get_by_id(id)
        if not item:
            return {"message": f"Product with id {id} not found"}, 404
        item = ProductService.delete(id)
        return f"successfully deleted product with id {id}", 200

# api/products
class ProductListResource(Resource):
    @marshal_with(marshal_fields)
    def get(self):
        items = ProductService.get_all()
        return (items)
    
    @marshal_with(marshal_fields)
    def post(self):
        args = parser.parse_args()
        item = ProductService.create(args)
        return item, 201