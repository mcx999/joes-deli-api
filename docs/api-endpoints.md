\# API Endpoints



This document lists the major API endpoints available in the Joe’s Deli backend, grouped by feature area.



\---



\## Menu Endpoints



| Method | Endpoint        | Description                  | Access          |

|--------|------------------|------------------------------|------------------|

| GET    | /menu/           | List all menu items          | All users        |

| POST   | /menu/           | Create a new menu item       | Manager, Admin   |

| GET    | /menu/<id>/      | Retrieve a menu item         | All users        |

| PATCH  | /menu/<id>/      | Update a menu item           | Manager, Admin   |

| DELETE | /menu/<id>/      | Delete a menu item           | Manager, Admin   |



\---



\## Cart Endpoints



| Method | Endpoint          | Description                     | Access     |

|--------|--------------------|---------------------------------|------------|

| GET    | /cart/             | View items in cart              | Customer   |

| POST   | /cart/             | Add item to cart                | Customer   |

| DELETE | /cart/<id>/        | Remove item from cart           | Customer   |

| POST   | /cart/clear/       | Clear entire cart               | Customer   |



\---



\## Order Endpoints



| Method | Endpoint          | Description                               | Access                    |

|--------|--------------------|-------------------------------------------|----------------------------|

| GET    | /orders/           | List orders (filtered by role)            | Customer, Manager, Crew, Admin |

| POST   | /orders/           | Place a new order                         | Customer                  |

| GET    | /orders/<id>/      | Retrieve order details                    | Assigned Crew, Manager, Admin |

| PATCH  | /orders/<id>/      | Update order status or assignment         | Manager, Crew, Admin      |

| DELETE | /orders/<id>/      | Delete an order                           | Manager, Admin            |



\---



\## Ratings Endpoints



| Method | Endpoint          | Description                     | Access     |

|--------|--------------------|---------------------------------|------------|

| POST   | /ratings/          | Submit a rating for a menu item | Customer   |

| GET    | /ratings/          | List ratings                    | All users  |



\---



\## Authentication Endpoints



| Method | Endpoint             | Description                     |

|--------|-----------------------|---------------------------------|

| POST   | /api/token/          | Obtain access + refresh tokens  |

| POST   | /api/token/refresh/  | Refresh access token            |



\---



\## User \& Role Management (Admin Only)



| Method | Endpoint                | Description                     |

|--------|--------------------------|---------------------------------|

| GET    | /users/                  | List all users                  |

| POST   | /users/                  | Create a new user               |

| PATCH  | /users/<id>/             | Update user details             |

| DELETE | /users/<id>/             | Delete a user                   |

| POST   | /groups/assign/          | Assign user to a role group     |



\---



\## Notes



\- All authenticated requests require:  Authorization: Bearer <ACCESS\_TOKEN>



\- Role-based filtering ensures users only see what they are allowed to see.

\- Delivery crew can only view or update orders assigned to them.







