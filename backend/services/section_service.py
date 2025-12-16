from models import Section, db
from .service_errors import ServiceError

model = Section

class SectionService():

    @staticmethod
    # staticmethod basically means this method belongs to the class and not to any specific instance of the class.
    # This means you can directly call this method on the class itself without creating an instance of the class.
    # for example, you can call ProductService.get_all() without needing to do something like:
    # service = ProductService()
    def get_all():
        return model.query.all()
    
    @staticmethod
    def get_by_id(id):
        item = model.query.get(id)
        if (not item):
            raise ServiceError(f"Product with id {id} not found")
        return item
    
    @staticmethod
    def delete(id):
        item = model.query.get(id)
        if (not item):
            raise ServiceError(f"Product with id {id} not found")
        
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Product with id {id} deleted successfully"}

    @staticmethod
    def update(data):
        item = model.query.get(data["id"])
        if (not item):
            raise ServiceError(f"Product with id {data['id']} not found")
        
        # need check if key is present in model
        for key in data:
            setattr(item, key, data[key])

        db.session.commit()
        return item

    @staticmethod
    def create(data):
        item = model(**data)
        db.session.add(item)
        db.session.commit()
        return item