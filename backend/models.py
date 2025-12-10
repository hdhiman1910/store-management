from extensions import db
from datetime import datetime, timezone

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)

    requests = db.relationship('Request', back_populates="user")

class Request(BaseModel):
    data = db.Column(db.JSON)
    status = db.Column(db.Enum("approved", "rejected", "created"))
    type = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) # user id of manager who 

    user = db.relationship("User", back_populates='requests')

class Section(BaseModel):
    name = db.Column(db.String(20), nullable=False)

    products = db.relationship('Product', back_populates = 'section')

class Product(BaseModel):
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Numeric(10, 2))
    expiry = db.Column(db.DateTime(timezone=True))
    unit_of_sale = db.Column(db.Enum("litre", "unit", "kg"))

    section_id = db.Column(db.Integer(), db.ForeignKey("section.id"))

    # Relationship
    products = db.relationship('Product', backpopulates = 'section')


