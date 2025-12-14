from models import Product, db
from .service_errors import ServiceError

class ProductService():

    @staticmethod
    # staticmethod basically means this method belongs to the class and not to any specific instance of the class.
    # This means you can directly call this method on the class itself without creating an instance of the class.
    # for example, you can call ProductService.get_all() without needing to do something like:
    # service = ProductService()
    def get_all():
        return Product.query.all()
    
    @staticmethod
    def get_by_id(id):
        item = Product.query.get(id)
        if (not item):
            raise ServiceError(f"Product with id {id} not found")
        return item
    
    @staticmethod
    def delete(id):
        item = Product.query.get(id)
        if (not item):
            raise ServiceError(f"Product with id {id} not found")
        
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def update(data):
        item = Product.query.get(data["id"])
        if (not item):
            raise ServiceError(f"Product with id {data['id']} not found")
        
        item.name = data["name"]
        item.price = data["price"]
        item.description = data["description"]
        db.session.commit()

    @staticmethod
    def create(data):
        item = Product(
            name = data["name"],
            price = data["price"],
            description = data["description"]
        )
        db.session.add(item)
        db.session.commit()
        return item