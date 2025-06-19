from app import models
from app.database import SessionLocal
from datetime import datetime
import random
import sys

def load_data():
    """Used by main.py to safely auto-load when DB is empty."""
    if "--auto" not in sys.argv:
        sys.argv.append("--auto")
    main()

def main():
    db = SessionLocal()
    models.Base.metadata.create_all(bind=db.bind)

    force = "--force" in sys.argv
    auto = "--auto" in sys.argv

    if db.query(models.Customer).first():
        if force:
            print("Force flag detected. Deleting existing data...")
            db.query(models.OrderItem).delete()
            db.query(models.Order).delete()
            db.query(models.Address).delete()
            db.query(models.Customer).delete()
            db.commit()
        elif auto:
            print("Sample data already exists. Auto-load skipped.")
            return
        else:
            print("Sample data already loaded. Use --force to reload.")
            return

    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve","Frank","Grace","Henry","Isabella","Jack"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
    zip_codes = ["94110", "10001", "60614", "30301", "75201","95601","94101","94551","94765","07029","94279"]
    item_names = ["Chair", "Table", "Lamp", "Sofa", "Desk","Couch","Bed","Pillow","Blanket","Rug"]
    streets = ["123 Main St", "456 Elm Ave", "789 Oak Dr", "321 Maple Rd", "654 Pine Blvd","101 Sunrise Blvd", "202 Birchwood Ln", "303 Riverwalk Dr", "404 Aspen Ct", "505 Highland Ave",
                    "606 Willow Creek Rd", "707 Magnolia Blvd", "808 Cypress Ct", "202 Birchwood Ln", "303 Riverwalk Dr", "404 Aspen Ct"]
    cities = ["San Francisco", "New York", "Chicago", "Austin", "Seattle", "Los Angeles", "San Diego", "Dallas", "San Jose", "Houston"]
    states = ["CA", "NY", "IL", "TX", "WA"]
    year_list = list(range(2015, 2026)) 
    for i in range(1, 101):
        first = first_names[i % len(first_names)]
        last = last_names[i % len(last_names)]
        email = f"{first.lower()}{i}@gmail.com"
        phone = f"{random.choice(['212', '415', '312', '617', '305', '602', '412', '213', '206', '404'])}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


        customer = models.Customer(
            first_name=first,
            last_name=last,
            email=email,
            phone=phone
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        

        for _ in range(random.randint(1, 3)):
            billing_zip = random.choice(zip_codes)

            billing_address = models.Address(
                type="billing",            
                street = random.choice(streets),
                city = random.choice(cities),
                state = random.choice(states),
                zip_code=billing_zip,
                country="USA"
            )
            db.add(billing_address)
            db.commit()
            year = year_list[i % len(year_list)]  # Distributes evenly across years
            order = models.Order(
            customer_id=customer.id,
            billing_address_id=billing_address.id,
            timestamp=datetime(year, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23)),
            in_store=random.choice([True, False])
        )

            
            db.add(order)
            db.commit()
            db.refresh(order)

            for _ in range(random.randint(1, 4)):
                shipping_zip = random.choice(zip_codes)
                shipping_address = models.Address(
                    type="shipping",
                    street = random.choice(streets),
                    city = random.choice(cities),
                    state = random.choice(states),
                    zip_code=shipping_zip,
                    country="USA"
                )
                db.add(shipping_address)
                db.commit()

                item = models.OrderItem(
                    order_id=order.id,
                    item_name=random.choice(item_names),
                    shipping_address_id=shipping_address.id
                )
                db.add(item)
            db.commit()

    print("Sample data loaded successfully.")

if __name__ == "__main__":
    main()
