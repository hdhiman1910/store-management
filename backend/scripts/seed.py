import uuid
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from app import app
from flask_security import hash_password
from models import db, User, Role, UserRoles, Customer, Section, Product, Sale, SaleItem, Manager

fake = Faker("en_IN")

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed Users
        print("Creating roles...")
        roles = {
            "admin": Role(name="admin", description="super user"),
            "manager": Role(name="manager", description="handles and manages store"),
            "customer": Role(name="customer", description="buys items from store")
        }

        db.session.add_all(roles.values())
        db.session.commit()

        print("Creating admin user...")

        admin_user = User(
            email="admin@store.com",
            name="admin",
            password=hash_password('pass'),
            fs_uniquifier=str(uuid.uuid4())
        )

        db.session.add(admin_user)
        db.session.commit()

        db.session.add(UserRoles(user_id=admin_user.id, role_id=roles["admin"].id))
        db.session.commit()

        print("Creating manager user...")

        managers = []

        for i in range(5):
            user = User(
                email=fake.unique.email(),
                name=fake.name(),
                password=hash_password('pass'),
                active=False,
                fs_uniquifier=str(uuid.uuid4())
                )
            
            db.session.add(user)
            db.session.flush()

            db.session.add(UserRoles(user_id=user.id, role_id=roles["manager"].id))

            mgr = Manager(
                salary=random.randint(100000, 200000),
                address=fake.address(),
                department=fake.word().title(),
                user_id=user.id
            )
            db.session.add(mgr)
            managers.append(user)

        db.session.commit()

        print("Creating customer users...")

        customer = []
        for i in range(20):
            user = User(
                email=fake.unique.email(),
                name=fake.name(),
                password=hash_password('pass'),
                fs_uniquifier=str(uuid.uuid4())
            )
            db.session.add(user)
            db.session.flush()

            db.session.add(UserRoles(user_id=user.id, role_id=roles["customer"].id))

            cust = Customer(
                loyalty_points=random.randint(0, 1000),
                user_id=user.id
            )
            db.session.add(cust)
            customer.append(user)

        db.session.commit()

        print("Creating sections...")
        section_names = ["Beverages", "Bakery", "Produce", "Dairy", "Meat", "Seafood", "Frozen Foods", "Snacks", "Household Supplies", "Personal Care"]
        sections = []
        for name in section_names:
            s = Section(name=name)
            db.session.add(s)
            sections.append(s)
        db.session.commit()

        print("Creating products...")
        products = []
        for s in sections:
            for _ in range(10):
                p = Product(
                    name=fake.word() + " " + fake.word(),
                    description=fake.sentence(nb_words=10),
                    price=round(random.uniform(10.0, 500.0), 2),
                    stock=random.randint(10, 100),
                    section_id=s.id,
                    expiry = datetime.now(timezone.utc) + timedelta(days=random.randint(30, 365)),
                    mfd = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30)),
                    unit_of_measure=random.choice(['kg', 'litre', 'piece', 'pack'])
                )
                db.session.add(p)
                products.append(p)
        db.session.commit()

        print("Creating sales and sale items...")
        sales = []
        now = datetime.now(timezone.utc)
        for _ in range(30):
            sale_date = now - timedelta(days=random.randint(0, 30), hours=random.randint(0,23), minutes=random.randint(0,59))
            sale = Sale(
                created_at=sale_date,
                total_amount=0.0
            )
            db.session.add(sale)
            db.session.flush()

            num_items = random.randint(1, 5)
            total_amount = 0.0
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                price_at_sale = product.price

                sale_item = SaleItem(
                    quantity=quantity,
                    price_at_sale=price_at_sale,
                    product_id=product.id,
                    sale_id=sale.id
                )
                db.session.add(sale_item)

                total_amount += quantity * float(price_at_sale)

            sale.total_amount = round(total_amount, 2)
            sales.append(sale)

        db.session.commit()
        print("Database seeding completed.")

if __name__ == "__main__":
    seed_database()