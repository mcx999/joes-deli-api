# Joe’s Deli API

Joe’s Deli API is a production‑grade Django REST Framework backend powering a modern deli ordering system. It supports customers browsing the menu and placing orders, managers overseeing operations, delivery crew fulfilling orders, and admins managing users and groups.

This project demonstrates:

- Clean Django REST Framework architecture  
- Robust role‑based permissions  
- Secure JWT authentication  
- A realistic, fully seeded deli menu  
- A hardened test suite (103 passing tests)  
- Professional migrations and data modeling  
- Clear separation of concerns and reproducible workflows  

It is designed to be both a portfolio showcase and a foundation for a full‑stack application.

---

## Features

### Authentication & Roles
- JWT login & refresh  
- Four user roles: Customer, Manager, DeliveryCrew, Admin  
- Automatic test user creation  
- Strict permission scoping  

### Menu Management
- Browse menu items  
- Filter by category, price, search terms  
- Vegetarian/vegan flags  
- Managers/admins can add, update, delete items  
- Fully curated deli menu  

### Cart & Ordering
- Add/remove items from cart  
- Place orders  
- Delivery crew updates order status  
- Managers/admins assign delivery crew  

### Ratings
- Customers can rate menu items  
- Prevents duplicate ratings  
- Supports listing and filtering  

### Developer Experience
- 103‑test backend suite  
- Postman collection  
- Clean migrations  
- Clear project structure  

---

## Architecture

### High‑Level System Diagram

~~~mermaid
flowchart LR
    A[Next.js Frontend] -->|HTTPS / JSON| B[Django REST API]
    B --> C[SQLite3 Database]
    B --> D[JWT Auth System]
~~~

### Request Lifecycle

~~~mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant DB as Database

    U->>F: Place Order
    F->>A: POST /orders/
    A->>A: Validate JWT + permissions
    A->>DB: Create Order + Items
    DB-->>A: OK
    A-->>F: 201 Created
    F-->>U: Confirmation
~~~

### Role‑Based Access Flow

~~~mermaid
flowchart TD
    A[Incoming Request] --> B[Extract JWT]
    B --> C[Identify Role]
    C --> D{Allowed?}
    D -->|Yes| E[Execute View]
    D -->|No| F[403 Forbidden]
~~~

---

## Quickstart

~~~bash
git clone https://github.com/mcx999/JoesDeliDRF.git
cd JoesDeliDRF
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata menu_items.json
python manage.py create_test_users
python manage.py runserver
~~~

API available at: http://localhost:8000/


---

## Try It Now (cURL Quickstart)

### Login as Customer
~~~bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"customer","password":"password123"}'
~~~

### Get Menu
~~~bash
curl http://localhost:8000/menu/
~~~

### Authenticated Request
~~~bash
curl http://localhost:8000/cart/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
~~~

---

## Documentation

See the `/docs/` folder for:

- API Endpoints  
- Setup Guide  
- Test Users & JWT Auth  
- Role Matrix  
- Postman Walkthrough  
- Architecture  
- Data Model  
- Future Enhancements  

---

## License

MIT License — see `LICENSE`.


