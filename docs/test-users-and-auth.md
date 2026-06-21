\# Test Users \& JWT Authentication



This guide explains:



\- Test users  

\- JWT login  

\- Access + refresh tokens  

\- Authenticated requests  

\- Token refresh  

\- Common errors  



\---



\## Test Users



| Role          | Username | Password     |

|---------------|----------|--------------|

| Customer      | customer | password123  |

| Manager       | manager  | password123  |

| Delivery Crew | delivery | password123  |

| Admin (staff) | admin    | password123  |



\---



\## Obtain Tokens



Send a POST request to obtain access and refresh tokens:



\~\~\~json

POST /api/token/

{

&#x20; "username": "customer",

&#x20; "password": "password123"

}

\~\~\~



Response:



\~\~\~json

{

&#x20; "access": "<ACCESS\_TOKEN>",

&#x20; "refresh": "<REFRESH\_TOKEN>"

}

\~\~\~



\---



\## Authenticated Request



Include the access token in the `Authorization` header: Authorization: Bearer <ACCESS\_TOKEN>





Example:



\~\~\~bash

curl http://localhost:8000/cart/ \\

&#x20; -H "Authorization: Bearer <ACCESS\_TOKEN>"

\~\~\~



\---



\## Refresh Token



Use the refresh token to obtain a new access token:



\~\~\~json

POST /api/token/refresh/

{

&#x20; "refresh": "<REFRESH\_TOKEN>"

}

\~\~\~



Response:



\~\~\~json

{

&#x20; "access": "<NEW\_ACCESS\_TOKEN>"

}

\~\~\~



\---



\## Common Errors



| Error | Meaning | Fix |

|-------|---------|------|

| 401 | Missing/expired token | Login or refresh |

| 403 | Permission denied | Use correct role |

| 400 | Bad JSON | Fix request body |









