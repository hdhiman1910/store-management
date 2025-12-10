from app import app
from models import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

# run this from "backend" folder using command: python -m scripts.init_db

with app.app_context():
    db.drop_all() 
    db.create_all()
    datastore : SQLAlchemyUserDatastore = app.datastore

    admin_role = datastore.find_or_create_role("admin", description = "super user")
    manager_role = datastore.find_or_create_role("manager", description = "handles and manges store")
    customer_role = datastore.find_or_create_role("customer", description = "buys items from store")

    if not datastore.find_user(email = "admin@store"):
        datastore.create_user(
            email = "admin@store",
            name = "admin_01",
            password = hash_password('pass'),
        )
    if not datastore.find_user(email = "manager@store"):
        datastore.create_user(
            email = "manager@store",
            name = "manager_01",
            password = hash_password('pass'),
        )
    if not datastore.find_user(email = "customer@store"):
        datastore.create_user(
            email = "customer@store",
            name = "customer_01",
            password = hash_password('pass'),
        )


    try:
        db.session.commit()
        print("Created successfully")
    except:
        db.session.rollback()
        print("Error while creating ref. line 40 of init_db.py")

    admin01 = datastore.find_user(email="admin@store")
    manager01 = datastore.find_user(email="manager@store")
    cust = datastore.find_user(email="customer@store")

    admin_role = datastore.find_role("admin")
    manager_role = datastore.find_role("manager")
    customer_role = datastore.find_role("customer")

    datastore.add_role_to_user(admin01, admin_role)
    datastore.add_role_to_user(manager01, manager_role)
    datastore.add_role_to_user(cust, customer_role)

    try:
        db.session.commit()
        print("Successfully Added roles")
    except:
        db.session.rollback()
        print("Error adding roles, refer to line 62 of scripts/init_db.py")