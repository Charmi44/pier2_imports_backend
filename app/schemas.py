"""
Pydantic schemas for request/response models.
Defines validation and serialization logic for API.
"""

from pydantic import BaseModel
from typing import List
from datetime import datetime

class Address(BaseModel):
    """
    Pydantic model for Address used in billing, shipping, or customer profile.
    """
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    type: str 

class OrderItem(BaseModel):
    """
    Represents a single item in an order, along with its shipping address.
    """
    item_name: str
    shipping_address: Address

class Order(BaseModel):
    """
    Represents a full order including billing address, timestamp, and items.
    """
    timestamp: datetime
    billing_address: Address
    in_store: bool
    items: List[OrderItem]

class Customer(BaseModel):
    """
    Customer data including basic info and reusable schema for display.
    """
    first_name: str
    last_name: str
    email: str
    phone: str
    addresses: List[Address]