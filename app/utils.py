from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal
from faker import Faker
import random

faker = Faker()

def create_sample_data(db: Session, num_customers: int = 100):
    for _ in range(num_customers):
        customer = models.Customer(
            email=faker.unique.email(),
            phone=faker.unique.phone_number(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

        shipping_address = models.Address(
            street=faker.street_address(),
            city=faker.city(),
            state=faker.state_abbr(),
            zip_code=faker.zipcode(),
            country="USA",
            type="shipping",
            customer_id=customer.id,
        )
        billing_address = models.Address(
            street=faker.street_address(),
            city=faker.city(),
            state=faker.state_abbr(),
            zip_code=faker.zipcode(),
            country="USA",
            type="billing",
            customer_id=customer.id,
        )
        db.add_all([shipping_address, billing_address])
        db.commit()

        for _ in range(random.randint(1, 5)):
            order = models.Order(
                customer_id=customer.id,
                billing_address_id=billing_address.id,
                in_store=random.choice([True, False]),
            )
            db.add(order)
            db.commit()
            db.refresh(order)

            for _ in range(random.randint(1, 3)):
                item = models.OrderItem(
                    order_id=order.id,
                    item_name=faker.word(),
                    shipping_address_id=shipping_address.id
                )
                db.add(item)
            db.commit()
            
def get_sample_data():
    db = SessionLocal()
    customers = db.query(models.Customer).limit(5).all()
    return [
        {
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone
        }
        for c in customers
    ]