\# Architecture



This document provides a high‑level overview of the architecture behind the Joe’s Deli API, including system components, request flow, and internal structure.



\---



\## System Overview



The backend is built using:



\- \*\*Django\*\* — project framework  

\- \*\*Django REST Framework (DRF)\*\* — API layer  

\- \*\*SQLite\*\* — local development database  

\- \*\*JWT Authentication\*\* — secure token‑based auth  

\- \*\*Role‑Based Permissions\*\* — enforced at the view level  



\---



\## High‑Level Architecture Diagram



\~\~\~mermaid

flowchart LR

&#x20;   A\[Next.js Frontend] -->|HTTPS / JSON| B\[Django REST API]

&#x20;   B --> C\[SQLite Database]

&#x20;   B --> D\[JWT Auth System]

&#x20;   B --> E\[Role-Based Permissions]

\~\~\~



\---



\## Request Lifecycle



1\. Client sends HTTP request  

2\. Django routes request to the correct DRF view  

3\. JWT authentication validates the token  

4\. Permissions determine whether the user may proceed  

5\. View executes business logic  

6\. Serializer validates and transforms data  

7\. Response returned as JSON  



\---



\## Request Flow Diagram



\~\~\~mermaid

sequenceDiagram

&#x20;   participant U as User

&#x20;   participant F as Frontend

&#x20;   participant A as API

&#x20;   participant DB as Database



&#x20;   U->>F: Submit Request

&#x20;   F->>A: API Call

&#x20;   A->>A: Validate JWT + Permissions

&#x20;   A->>DB: Query/Update Data

&#x20;   DB-->>A: Result

&#x20;   A-->>F: JSON Response

&#x20;   F-->>U: Rendered Output

\~\~\~



\---



\## Directory Structure



\~\~\~text

JoesDeliDRF/

│

├── JoesDeliDRF/          # Django project settings

├── api/                  # Core API app

│   ├── views.py          # View logic

│   ├── serializers.py    # Data validation \& transformation

│   ├── models.py         # Database models

│   ├── permissions.py    # Role-based access control

│   ├── urls.py           # Endpoint routing

│   └── tests/            # 103 test cases

│

├── menu\_items.json       # Seed data

├── requirements.txt      # Dependencies

└── manage.py             # Django CLI entry point

\~\~\~



\---



\## Key Components



\### Models

\- MenuItem  

\- CartItem  

\- Order  

\- OrderItem  

\- Rating  



\### Views

\- MenuViewSet  

\- CartView  

\- OrderViewSet  

\- RatingView  



\### Permissions

\- IsCustomer  

\- IsManager  

\- IsDeliveryCrew  

\- IsAdmin  



\### Authentication

\- JWT Access Tokens  

\- JWT Refresh Tokens  



\---



\## Data Flow Summary



1\. \*\*Frontend\*\* sends JSON request  

2\. \*\*API\*\* authenticates and authorizes  

3\. \*\*View\*\* executes logic  

4\. \*\*Serializer\*\* validates input/output  

5\. \*\*Database\*\* stores or retrieves data  

6\. \*\*API\*\* returns JSON response  



\---



\## Notes



\- The architecture is intentionally simple and clean for learning and portfolio use.  

\- The system is fully compatible with PostgreSQL for production deployment.  



