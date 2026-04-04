# Joe's Deli API

Joe's Deli API is a production grade backend for a modern deli ordering system. It supports customers browsing the menu and placing orders, managers overseeing operations, delivery crew fulfilling orders, and admins managing users and groups.

This project demonstrates:

- Clean Django REST Framework architecture
- Robust role based permissions
- Secure JWT authentication
- A realistic, fully seeded deli menu
- A hardened test suite (103 passing tests)
- Professional migrations and data modeling
- Clear separation of concerns and reproducible workflows

It's designed to be both a portfolio showcase and a foundation for a full stack application.

---

## 🚀 Features

### 👤 Authentication & Roles

- JWT login & refresh
- Four user roles:
  - Customer
  - Manager
  - DeliveryCrew
  - Admin (staff)
- Automatic test user creation for each role

### 🧾 Menu Management

- Browse menu items
- Filter by category, price, search terms
- Vegetarian/vegan flags
- Managers/admins can add, update, or delete items
- Fully curated deli menu with soups, sandwiches, sides, beverages, and desserts

### 🛒 Cart & Ordering

- Customers can add/remove items from their cart
- Place orders from cart
- Order items created automatically
- Delivery crew can update order status
- Managers/admins can assign delivery crew

### ⭐ Ratings

- Customers can rate menu items
- Prevents duplicate ratings
- Supports listing and filtering

### 🔐 Permissions

- Strict scoping:
  - Customers only see their own orders
  - Delivery crew only see assigned orders
  - Managers/admins see everything
- Comprehensive permission tests

### 🧪 Test Suite

- 103 tests covering:
  - Permissions
  - Authentication
  - Menu filtering
  - Cart behavior
  - Order workflows
  - Pagination
  - JWT auth
  - Group management
- Fully passing

---

## Project Structure

```
JoesDeliDRF/
├── JoesDeliDRF/          # Core project settings
├── api/                  # Viewsets, serializers, permissions
├── management/           # Test user creation command
├── migrations/           # Database migrations
├── tests/                # Comprehensive test suite
└── fixtures/             # Seeded menu data
```

---

## Seeded Menu

Joe's Deli includes a fully curated, realistic menu with:

- 11 soups
- 18 sandwiches
- 6 sides
- 6 desserts
- 6 beverages

All items include:

- Price
- Description
- Category
- Vegetarian/vegan flags

This makes the API feel like a real restaurant backend.

---

## What You Can Do With This Project

Once this repo is public, users will be able to:

- ✔ Clone it
- ✔ Run it locally
- ✔ Explore the API
- ✔ Authenticate as different roles
- ✔ Place orders
- ✔ Manage menu items
- ✔ Assign delivery crew
- ✔ Run the full test suite
- ✔ Fork it and build on it

This backend is intentionally designed to be a platform for further development.

---

## Installation & Setup

**1. Clone the repo**

```bash
git clone https://github.com/yourusername/JoesDeliDRF.git
cd JoesDeliDRF
```

**2. Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Run Migrations**

```bash
python manage.py migrate
```

**5. Load the seeded menu (optional)**

```bash
python manage.py loaddata menu_items.json
```

**6. Create test users**

```bash
python manage.py create_test_users
```

**7. Run the server**

```bash
python manage.py runserver
```

**8. Authentication**

Use the JWT endpoint:

```http
POST /api/token/
{
  "username": "customer",
  "password": "password123"
}
```

You'll receive:

- `access` token
- `refresh` token

Use the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

---

## 9. API Endpoints (Summary)

### Menu

| Method | Endpoint | Access |
|--------|----------|--------|
| `GET` | `/menu/` | All |
| `POST` | `/menu/` | Manager/Admin |
| `GET` | `/menu/<id>/` | All |
| `PATCH` | `/menu/<id>/` | Manager/Admin |

Filtering: `?category=`, `?search=`, `?ordering=price`

### Cart

| Method | Endpoint | Access |
|--------|----------|--------|
| `GET` | `/cart/` | Customer |
| `POST` | `/cart/` | Customer |
| `DELETE` | `/cart/<id>/` | Customer |
| `POST` | `/cart/clear/` | Customer |

### Orders

| Method | Endpoint | Access |
|--------|----------|--------|
| `GET` | `/orders/` | All |
| `POST` | `/orders/` | Customer |
| `PATCH` | `/orders/<id>/` | Manager/Admin/Crew |
| `DELETE` | `/orders/<id>/` | Manager/Admin |

### Ratings

| Method | Endpoint | Access |
|--------|----------|--------|
| `GET` | `/ratings/` | All |
| `POST` | `/ratings/` | Customer |

### Group Management

| Method | Endpoint | Access |
|--------|----------|--------|
| `GET` | `/groups/` | Manager/Admin |
| `POST` | `/groups/<name>/users/` | Manager/Admin |
| `DELETE` | `/groups/<name>/users/<id>/` | Manager/Admin |

---

## 🧪 Running Tests

```bash
python manage.py test
```

All 103 tests should pass.

---

## 🧭 Roadmap

### Completed

- Core backend
- Role system
- JWT auth
- Menu + ordering
- Security fixes
- 103 test suite
- Menu refinement
- Migration updates

### Current (PI 3)

- README
- Documentation
- Repo polish
- LICENSE

### Future Enhancements

- Swagger/OpenAPI docs
- Docker support
- GitHub Actions CI
- Postman collection
- Frontend UI (React/Next.js)
- Deployment (Render/Vercel)
- Analytics dashboard
- Loyalty program
- Mobile app

---

## 📄 License

MIT License *(will be added once repo is created)*

---

## 🙌 Credits

Built by Michael, with a focus on clarity, reproducibility, and professional engineering practices.
