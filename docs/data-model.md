\# Data Model



This document describes the database schema used by the Joe’s Deli API, including models, relationships, and diagrams.



\---



\## Overview of Models



The backend uses the following core models:



\- \*\*MenuItem\*\* — Represents a deli menu item  

\- \*\*CartItem\*\* — Items added to a customer’s cart  

\- \*\*Order\*\* — A placed order  

\- \*\*OrderItem\*\* — Items within an order  

\- \*\*Rating\*\* — Customer ratings for menu items  

\- \*\*User\*\* — Django auth user  

\- \*\*Groups\*\* — Role-based access control  



\---



\## Entity Relationship Diagram (ERD)



\~\~\~mermaid

erDiagram



&#x20;   USER ||--o{ CARTITEM : "has"

&#x20;   USER ||--o{ ORDER : "places"

&#x20;   USER ||--o{ RATING : "writes"



&#x20;   MENUITEM ||--o{ CARTITEM : "added to"

&#x20;   MENUITEM ||--o{ ORDERITEM : "included in"

&#x20;   MENUITEM ||--o{ RATING : "rated by"



&#x20;   ORDER ||--o{ ORDERITEM : "contains"



&#x20;   USER ||--o{ ORDER : "assigned as delivery crew"

\~\~\~



\---



\## MenuItem



Represents a single deli menu item.



\### Fields



| Field        | Type      | Description                     |

|--------------|-----------|---------------------------------|

| title        | string    | Name of the item                |

| price        | decimal   | Price of the item               |

| category     | string    | Category (sandwich, salad, etc.)|

| description  | text      | Optional description            |

| is\_vegan     | boolean   | Vegan flag                      |

| is\_vegetarian| boolean   | Vegetarian flag                 |



\---



\## CartItem



Represents an item in a customer’s cart.



\### Fields



| Field     | Type      | Description                |

|-----------|-----------|----------------------------|

| user      | FK(User)  | Owner of the cart          |

| menu\_item | FK(MenuItem) | Item added              |

| quantity  | integer   | Quantity selected          |



\---



\## Order



Represents a placed order.



\### Fields



| Field          | Type        | Description                          |

|----------------|-------------|--------------------------------------|

| user           | FK(User)    | Customer who placed the order        |

| delivery\_crew  | FK(User)    | Assigned delivery crew member        |

| status         | integer     | 0 = pending, 1 = out for delivery…   |

| total          | decimal     | Total price                          |

| date           | datetime    | Timestamp                            |



\---



\## OrderItem



Represents a single item within an order.



\### Fields



| Field     | Type          | Description                |

|-----------|---------------|----------------------------|

| order     | FK(Order)     | Parent order               |

| menu\_item | FK(MenuItem)  | Item ordered               |

| quantity  | integer       | Quantity                   |

| price     | decimal       | Price at time of order     |



\---



\## Rating



Represents a customer rating for a menu item.



\### Fields



| Field     | Type          | Description                |

|-----------|---------------|----------------------------|

| user      | FK(User)      | Customer who rated         |

| menu\_item | FK(MenuItem)  | Item being rated           |

| score     | integer       | Rating 1–5                 |

| comment   | text          | Optional comment           |



\---



\## Notes



\- Ratings enforce \*\*one rating per user per menu item\*\*.  

\- Order totals are calculated automatically.  

\- Delivery crew can only see orders assigned to them.  

\- Menu items are fully normalized and reusable across carts and orders.  



