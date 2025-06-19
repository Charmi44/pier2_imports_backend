"""
SQLAlchemy ORM models for Pier 2 backend system.
Defines database schema and relationships using declarative_base.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    """
    Represents a customer in the system.
    Each customer can place multiple orders and have multiple addresses (home, office, etc.).
    """
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")  


class Address(Base):
    """
    Represents an address in the system.
    Can be linked to a customer (e.g., home/office) or used for billing/shipping.
    """
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # 'home', 'office', 'billing', 'shipping'
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String, default="USA")

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)  # New FK to customer
    customer = relationship("Customer", back_populates="addresses")


class Order(Base):
    """
    Represents a customer's order.
    Each order has a billing address and may contain multiple items.
    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    billing_address_id = Column(Integer, ForeignKey("addresses.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    in_store = Column(Boolean)

    customer = relationship("Customer", back_populates="orders")
    billing_address = relationship("Address")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """
    Represents an item in an order.
    Each item has a name and shipping address.
    """
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_name = Column(String)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"))

    order = relationship("Order", back_populates="items")
    shipping_address = relationship("Address")
