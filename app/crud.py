from sqlalchemy.orm import Session
from sqlalchemy import func, text, desc, asc
from datetime import datetime
from app import models


def get_order_history(email_or_phone: str, db: Session):
    """
    Retrieve the full order history for a customer based on email or phone number.

    Args:
        email_or_phone (str): Customer identifier (email or phone).
        db (Session): SQLAlchemy database session.

    Returns:
        list or dict: List of orders or error message.
    """
    query = db.query(models.Customer)
    if "@" in email_or_phone:
        customer = query.filter(models.Customer.email == email_or_phone).first()
    else:
        customer = query.filter(models.Customer.phone == email_or_phone).first()

    if not customer:
        return {"error": "Customer not found"}

    history = []
    for order in customer.orders:
        order_data = {
            "order_id": order.id,
            "timestamp": order.timestamp.isoformat(),
            "in_store": order.in_store,
            "billing_address": {
                "street": order.billing_address.street,
                "city": order.billing_address.city,
                "state": order.billing_address.state,
                "zip_code": order.billing_address.zip_code,
                "country": order.billing_address.country
            },
            "items": [
                {
                    "item_name": item.item_name,
                    "shipping_address": {
                        "street": item.shipping_address.street,
                        "city": item.shipping_address.city,
                        "state": item.shipping_address.state,
                        "zip_code": item.shipping_address.zip_code,
                        "country": item.shipping_address.country
                    }
                } for item in order.items
            ]
        }
        history.append(order_data)

    return history


def get_orders_grouped_by_billing_zip(db: Session, order: str = "desc"):
    """
    Returns total count of orders grouped by billing zip code.

    Args:
        db (Session): SQLAlchemy DB session.
        order (str): "asc" or "desc" sort order.

    Returns:
        list[dict]: List of zip codes and order counts.
    """
    zip_counts = db.query(
        models.Address.zip_code,
        func.count(models.Order.id).label("order_count")
    ).join(
        models.Order, models.Order.billing_address_id == models.Address.id
    ).group_by(models.Address.zip_code)

    # Apply sort order
    zip_counts = zip_counts.order_by(
        text("order_count ASC") if order == "asc" else text("order_count DESC")
    )

    return [{"zip_code": row[0], "order_count": row[1]} for row in zip_counts.all()]


def get_orders_grouped_by_shipping_zip(db: Session, order: str = "desc"):
    """
    Returns total count of order items grouped by shipping zip code.

    Args:
        db (Session): SQLAlchemy DB session.
        order (str): "asc" or "desc" sort order.

    Returns:
        list[dict]: List of zip codes and item shipment counts.
    """
    zip_counts = db.query(
        models.Address.zip_code,
        func.count(models.OrderItem.id).label("order_count")
    ).join(
        models.OrderItem, models.OrderItem.shipping_address_id == models.Address.id
    ).group_by(models.Address.zip_code)

    zip_counts = zip_counts.order_by(
        asc("order_count") if order == "asc" else desc("order_count")
    )

    return [{"zip_code": row[0], "order_count": row[1]} for row in zip_counts.all()]


def get_peak_instore_purchase_hour(db: Session):
    """
    Identify the hour of the day with the most in-store purchases.

    Args:
        db (Session): SQLAlchemy DB session.

    Returns:
        dict: Peak hour (12-hour format) and count.
    """
    hourly_counts = {}
    orders = db.query(models.Order).filter(models.Order.in_store == True).all()

    for order in orders:
        hour = order.timestamp.hour
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1

    if not hourly_counts:
        return {}

    peak_hour = max(hourly_counts, key=hourly_counts.get)
    count = hourly_counts[peak_hour]
    label = f"{(peak_hour % 12 or 12)}{'am' if peak_hour < 12 else 'pm'}"

    return {label: count}


def get_top_instore_customer(db: Session, start_date: str = None, end_date: str = None):
    """
    Get top 5 customers with the most in-store orders, optionally within a date range.

    Args:
        db (Session): SQLAlchemy DB session.
        start_date (str): Optional filter in mm-dd-yyyy format.
        end_date (str): Optional filter in mm-dd-yyyy format.

    Returns:
        list[dict]: Top 5 customers with order counts.
    """
    query = db.query(
        models.Customer.email,
        models.Customer.first_name,
        models.Customer.last_name,
        models.Customer.phone,
        func.count(models.Order.id).label("in_store_count")
    ).join(models.Order).filter(
        models.Order.in_store == True
    )

    if start_date:
        start = datetime.strptime(start_date, "%m-%d-%Y")
        query = query.filter(models.Order.timestamp >= start)

    if end_date:
        end = datetime.strptime(end_date, "%m-%d-%Y")
        query = query.filter(models.Order.timestamp <= end)

    results = query.group_by(models.Customer.id).order_by(
        func.count(models.Order.id).desc()
    ).limit(5).all()

    return [
        {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "in_store_order_count": in_store_count
        }
        for email, first_name, last_name, phone, in_store_count in results
    ]
