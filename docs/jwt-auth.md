\# JWT Authentication



This document explains how JWT (JSON Web Token) authentication works in the Joe’s Deli API, including how to obtain tokens, refresh them, and use them in authenticated requests.



\---



\## Overview



The API uses \*\*JWT access tokens\*\* for authentication.  

Clients authenticate by including the access token in the `Authorization` header: Authorization: Bearer <ACCESS\_TOKEN>





Tokens are obtained via the `/api/token/` endpoint.



\---



\## Obtain Access \& Refresh Tokens



Send a POST request to: POST /api/token/





Body:



\~\~\~json

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



\- \*\*Access token\*\* → used for all authenticated requests  

\- \*\*Refresh token\*\* → used to obtain a new access token when the old one expires  



\---



\## Using the Access Token



Include the token in the header: Authorization: Bearer <ACCESS\_TOKEN>





Example:



\~\~\~bash

curl http://localhost:8000/orders/ \\

&#x20; -H "Authorization: Bearer <ACCESS\_TOKEN>"

\~\~\~



\---



\## Refreshing the Access Token



When the access token expires, request a new one: POST /api/token/refresh/





Body:



\~\~\~json

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



\## Token Expiration



\- Access tokens expire quickly (short‑lived for security).  

\- Refresh tokens last longer and can be used to obtain new access tokens.  

\- If both expire, the user must log in again.



\---



\## Common Errors



| Error | Meaning | Fix |

|-------|---------|------|

| 401 Unauthorized | Missing or expired access token | Refresh or log in again |

| 403 Forbidden | Token valid but user lacks permissions | Use correct role |

| 400 Bad Request | Invalid JSON or missing fields | Correct request body |



\---



\## Security Notes



\- Never expose refresh tokens in client‑side code.  

\- Always use HTTPS in production.  

\- Tokens should be stored securely (e.g., HTTP‑only cookies or secure storage).



















