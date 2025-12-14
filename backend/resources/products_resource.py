from flask import request, jsonify
from flask_restful import Resource
from services import ProductService


def serialize_product(item):
    return {
        "id": item.id,
        "name": item.name,
        "price": str(item.price) if item.price is not None else None,
        "description": item.description,
        "stock": str(item.stock) if item.stock is not None else None,
    }

class ProductResource(Resource):
    def get(self, id):
        item = ProductService.get_by_id(id)
        return jsonify(serialize_product(item))

class ProductListResource(Resource):
    def get(self):
        items = ProductService.get_all()
        return jsonify([serialize_product(i) for i in items])