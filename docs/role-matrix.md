# Role Matrix

This document outlines what each user role in the Joe’s Deli API is permitted to do.

---

## Role Capabilities Overview

| Action                     | Customer | Manager | Delivery Crew | Admin |
|----------------------------|----------|---------|----------------|--------|
| View Menu                  | ✔        | ✔       | ✔              | ✔      |
| Add/Edit Menu              | ✖        | ✔       | ✖              | ✔      |
| Manage Cart                | ✔        | ✖       | ✖              | ✖      |
| Place Orders               | ✔        | ✖       | ✖              | ✖      |
| View All Orders            | ✖        | ✔       | ✔ (assigned)   | ✔      |
| Assign Delivery Crew       | ✖        | ✔       | ✖              | ✔      |
| Update Order Status        | ✖        | ✖       | ✔              | ✔      |
| Manage Users/Groups        | ✖        | ✔       | ✖              | ✔      |

---

## Notes

- **Customers** can browse the menu, manage their cart, and place orders.  
- **Managers** can manage menu items, view all orders, and assign delivery crew.  
- **Delivery Crew** can only view and update orders assigned to them.  
- **Admins** have full access to all resources and management features.

