from flask_restful import fields

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

product_fields = {
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