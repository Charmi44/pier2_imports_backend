# Pier 2 Imports Backend
# Pier 2 Imports - Backend System

Welcome to the backend system for **Pier 2 Imports**, a home and office goods retailer with both online and in-store sales. This project provides a RESTful API built with **FastAPI** to manage customer orders, address data, and perform analytics.

---

## 🧠 Project Overview

This backend system is designed to:
- Maintain accurate and deduplicated **customer records** (by email or phone).
- Track **orders** placed either **online** (with delivery) or **in-store**.
- Handle complex **shipping logic**, such as **multiple shipping addresses per order**.
- Support analytics like:
  - Orders by **billing or shipping zip**
  - **Peak hours** for in-store purchases
  - **Top 5 customers** by in-store purchases

The API is self-contained using a **SQLite database**, with **sample data auto-loaded** on first run to demonstrate functionality.
⚠️ Note: The API runs on `http://localhost:8000/docs` locally. For production, configuring HTTPS using a reverse proxy like nginx or deploy behind a secure load balancer is more viable.

---

## 🚀 Getting Started

### 1. 📦 Requirements

- Python 3.8+
- `pip` (Python package manager)

### 2. 🔧 Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/Charmi44/pier2_backend.git
cd pier2_backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. ▶️ Run the API

```bash
bash run.sh
```

Access the API docs at:  
[http://localhost:8000/docs]
---

## 📊 API Endpoints (With Examples)

### 1. ✅ Health Check

```bash
curl http://localhost:8000/health
```

Code	
200	
Response body

{
  "status": "Backend is running"
}

---

### 2. 📦 Order History by Email/Phone

```bash

Request URL : http://localhost:8000/customer/charlie2%40gmail.com/orders

```
Response Body:
{"order_id":4,"timestamp":"2017-05-10T02:00:00","in_store":true,"billing_address":{"street":"707 Magnolia Blvd","city":"Los Angeles","state":"TX","zip_code":"94551","country":"USA"},"items":[{"item_name":"Pillow","shipping_address":{"street":"789 Oak Dr","city":"New York","state":"TX","zip_code":"94765","country":"USA"}},{"item_name":"Blanket","shipping_address":{"street":"101 Sunrise Blvd","city":"Dallas","state":"WA","zip_code":"94101","country":"USA"}},{"item_name":"Couch","shipping_address":{"street":"404 Aspen Ct","city":"Dallas","state":"NY","zip_code":"94551","country":"USA"}}]}]

---

### 3. 📈 Orders by Billing Zip (Descending)

```bash
curl "http://localhost:8000/analytics/orders_by_billing_zip?order=desc"
```
Response body: [{"zip_code":"94101","order_count":26},{"zip_code":"94765","order_count":23},{"zip_code":"94110","order_count":22},{"zip_code":"94551","order_count":20},{"zip_code":"95601","order_count":17},{"zip_code":"07029","order_count":17},{"zip_code":"94279","order_count":16},{"zip_code":"10001","order_count":15},{"zip_code":"30301","order_count":14},{"zip_code":"75201","order_count":13},{"zip_code":"60614","order_count":9}]
---

### 4. 🚚 Orders by Shipping Zip (Ascending)

```bash
curl "http://localhost:8000/analytics/orders_by_shipping_zip?order=asc"
```

Response body : [{"zip_code":"10001","order_count":33},{"zip_code":"60614","order_count":36},{"zip_code":"95601","order_count":38},{"zip_code":"94765","order_count":42},{"zip_code":"94279","order_count":43},{"zip_code":"30301","order_count":46},{"zip_code":"75201","order_count":48},{"zip_code":"94551","order_count":48},{"zip_code":"07029","order_count":49},{"zip_code":"94101","order_count":51},{"zip_code":"94110","order_count":51}]

---

### 5. 🕒 Peak In-Store Hour

```bash
curl http://localhost:8000/analytics/in_store_peak_hour
```

Example response:

```json
{
  "3pm": 12
}
```

---

### 6. 🏆 Top 5 In-Store Customers (Optionally filtered by date)

```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/analytics/top_instore_customers?start_date=01-01-2022&end_date=01-01-2025' \
  -H 'accept: application/json'
```

Example response:

```json
[
  [{"email":"grace86@gmail.com","first_name":"Grace","last_name":"Miller","phone":"212-897-2626","in_store_order_count":3},{"email":"bob51@gmail.com","first_name":"Bob","last_name":"Johnson","phone":"602-649-8783","in_store_order_count":3},{"email":"grace96@gmail.com","first_name":"Grace","last_name":"Miller","phone":"213-559-2263","in_store_order_count":2},{"email":"eve84@gmail.com","first_name":"Eve","last_name":"Jones","phone":"312-695-8515","in_store_order_count":2},{"email":"alice40@gmail.com","first_name":"Alice","last_name":"Smith","phone":"415-246-5299","in_store_order_count":2}]
]
```

---

## 🧪 Running Unit Tests

Ensure you are in the virtual environment, then run:

```bash
pytest tests/
```

The tests use `TestClient` and mocking to isolate FastAPI endpoints and validate expected results.

---

## 📁 Directory Structure

```
pier2_backend/
├── app/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── tests/
│   └── test_endpoints.py
├── load_sample_data.py
├── requirements.txt
├── run.sh
└── README.md
```

---

## 📌 Assumptions Made

| Topic | Assumption |
|-------|------------|
| Email/Phone change | Preserved in DB for audit, but not yet versioned |
| Customer lookup | Either email or phone (deduplicated) |
| Multiple shipping addresses | Supported at **order item level** |
| Address fields | Street, City, State, Zip, Country (US only) |
| In-store order time | Based on `timestamp.hour`, returned in 12hr format |
| Analytics period | Filterable by `MM-DD-YYYY` date format |
| Authentication | Not implemented (internal API) |
| Deployment | Intended to be containerized or deployed via FastAPI on GCP/AWS/Azure |


---

## 🧠 Design Reasoning

- **FastAPI** was selected for its speed, simplicity, and built-in UI.
- **SQLite** was used for portability in this project; can be swapped with PostgreSQL or MySQL.
- **SQLAlchemy ORM** used to abstract database operations with Python objects, enabling maintainable and database-agnostic development. Relationships between models (like Customer, Order, Address) are clearly defined and enforced through SQLAlchemy's declarative system
- **Data Modeling**:
  - `Customer` has many `Orders`.
  - `Order` has one `BillingAddress`, and many `OrderItems`.
  - Each `OrderItem` has its own `ShippingAddress`.
- **Sample data** is readable (no Faker), spans years 2015–2025, and avoids duplicates on rerun.
- **Auto-load sample data** only when DB is empty (first run).
- **Test coverage** focuses on endpoint behavior using mocking for DB isolation.

---

## 📦 Deployment Suggestion

For real deployment:

- Package app into Docker container
- Use PostgreSQL instead of SQLite
- Add CI/CD pipeline with GitHub Actions
- Deploy to cloud with:
  - **FastAPI + Gunicorn + Uvicorn** (e.g., via Docker)
  - Managed DB (AWS RDS / GCP Cloud SQL)

---

## 📬 Questions from Assessment (Answered)

- **How would you store the address data to accommodate these requirements?** 
Create a single, reusable addresses table.

Include a type field to tag the address as 'home', 'office', 'billing', or 'shipping'.

Use foreign keys to associate:

Each customer → many addresses (customer_id in addresses)

Each order → one billing address (billing_address_id in orders)

Each order item → one shipping address (shipping_address_id in order_items)

This schema enables:

A customer to have multiple homes/offices.

Each order to have a billing address.

Each item in a single order to be shipped to a different address. 

  Each `OrderItem` can have a different `shipping_address_id`.

- **How do you store addresses?**  
  In a normalized `Address` table: street, city, state, zip, country (US).

| Goal                                  | Solution                              |
| ------------------------------------- | ------------------------------------- |
| Track multiple addresses per customer | Link `addresses.customer_id` as FK    |
| Track billing address per order       | Use `orders.billing_address_id`       |
| Track shipping per item               | Use `order_items.shipping_address_id` |
| Keep address purpose distinguishable  | Include a `type` field in `addresses` |



---

## 🤖 AI Usage Disclosure

Portions of the sample data generation, testing code setup, and docstring were accelerated using LLM-powered tools. All core business logic, API integration, and database interactions were manually implemented and validated to ensure correctness and alignment with the assignment requirements

---


Please feel free to raise an issue or pull request on GitHub.





