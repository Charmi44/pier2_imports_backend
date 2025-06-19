from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from app import models, crud, database, utils
from app.database import get_db  # Dependency for DB session

# Create all tables if they do not exist
models.Base.metadata.create_all(bind=database.engine)

# ✅ Auto-load sample data if DB is empty
with Session(bind=database.engine) as session:
    if not session.query(models.Customer).first():
        try:
            from load_sample_data import load_data
            load_data()
            print("✅ Sample data loaded on first run.")
        except Exception as e:
            print("❌ Error while auto-loading data:", e)

# ✅ FastAPI App Initialization
app = FastAPI(title="Pier 2 Imports Backend API")

# ✅ Enable CORS (for local web frontend or third-party tools like Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health Check Endpoint
@app.get("/health")
def health_check():
    """Simple health check to verify backend is running."""
    return {"status": "Backend is running"}


# ✅ Get complete order history for a customer
@app.get("/customer/{email_or_phone}/orders")
def get_order_history(email_or_phone: str, db: Session = Depends(get_db)):
    """
    Retrieve full order history for a customer by email or phone.
    """
    return crud.get_order_history(email_or_phone, db)


# ✅ Analytics: Count of orders by billing zip code
@app.get("/analytics/orders_by_billing_zip")
def orders_by_billing_zip(
    order: str = Query("desc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    """
    Show total count of orders grouped by billing zip code.
    Supports ascending or descending sort order.
    """
    return crud.get_orders_grouped_by_billing_zip(db, order=order)


# ✅ Analytics: Count of orders by shipping zip code
@app.get("/analytics/orders_by_shipping_zip")
def orders_by_shipping_zip(
    order: str = Query("desc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    """
    Show total count of orders grouped by shipping zip code.
    Supports ascending or descending sort order.
    """
    return crud.get_orders_grouped_by_shipping_zip(db, order=order)


# ✅ Analytics: Most common hour for in-store purchases
@app.get("/analytics/in_store_peak_hour")
def in_store_peak_hour(db: Session = Depends(get_db)):
    """
    Identify the hour of day with the highest number of in-store purchases.
    Returns hour in 12-hour format (e.g., '3pm').
    """
    return crud.get_peak_instore_purchase_hour(db)


# ✅ Analytics: Top 5 customers with in-store purchases
@app.get("/analytics/top_instore_customers")
def top_instore_customer(
    start_date: Optional[str] = Query(None, description="Start date in MM-DD-YYYY format"),
    end_date: Optional[str] = Query(None, description="End date in MM-DD-YYYY format"),
    db: Session = Depends(get_db)
):
    """
    List top 5 customers (by number of in-store orders).
    Supports optional filtering by date range.
    """
    return crud.get_top_instore_customer(db, start_date=start_date, end_date=end_date)


# ✅ Development: Load and return sample data (for testing/demo)
@app.get("/sample_data")
def get_sample_data():
    """
    Returns sample data for the application.
    NOTE: This is primarily for demo/debug usage.
    """
    return utils.get_sample_data()
