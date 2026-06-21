# Setup Guide

This guide walks you through setting up the Joe’s Deli API backend locally for development, testing, or exploration.  
Each step includes a brief explanation of what it accomplishes.

---

## 1. Clone the Repository
Download the project from GitHub and move into its directory.

~~~bash
git clone https://github.com/mcx999/JoesDeliDRF.git
cd JoesDeliDRF
~~~

---

## 2. Create a Virtual Environment
Creates an isolated Python environment so dependencies do not interfere with your system Python.

~~~bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
~~~

---

## 3. Install Dependencies
Installs all required Python packages listed in `requirements.txt`.

~~~bash
pip install -r requirements.txt
~~~

---

## 4. Apply Database Migrations
Creates the SQLite database and applies all Django migrations to build the schema.

~~~bash
python manage.py migrate
~~~

---

## 5. Load Seed Data (Optional)
Loads the fully curated deli menu into the database so the API starts with realistic menu items.

~~~bash
python manage.py loaddata menu_items.json
~~~

---

## 6. Create Test Users
Creates sample accounts for each role (Customer, Manager, DeliveryCrew, Admin).

~~~bash
python manage.py create_test_users
~~~

---

## 7. Run the Development Server

~~~bash
python manage.py runserver
~~~

API available at: http://localhost:8000/


---

## Next Steps

See:

- `/docs/jwt-auth.md`  
- `/docs/test-users-and-auth.md`

