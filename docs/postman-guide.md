# Postman Guide

This guide explains how to use Postman to test the Joe’s Deli API, including authentication, environment setup, and running requests.

---

## Import the Postman Collection

1. Open Postman  
2. Click **Import**  
3. Select the file:  JoesDeliAPI.postman_collection.json


This collection includes all major endpoints:  
- Menu  
- Cart  
- Orders  
- Ratings  
- Authentication  

---

## Import the Postman Environment

1. In Postman, open the **Environments** tab  
2. Click **Import**  
3. Select:  JoesDeliAPI.postman_environment.json

4. Choose the environment in the top‑right dropdown

This environment stores:  
- `base_url`  
- `access_token`  
- `refresh_token`  

---

## Authenticate (Generate Tokens)

Use the **POST /api/token/** request in the collection.

Body:

~~~json
{
"username": "customer",
"password": "password123"
}
~~~

Postman will automatically store the returned tokens in environment variables.

---

## Using the Access Token

All authenticated requests in the collection automatically include: Authorization: Bearer {{access_token}}


You do not need to manually paste tokens.

---

## Refreshing the Token

Use the **POST /api/token/refresh/** request.

Body:

~~~json
{
  "refresh": "{{refresh_token}}"
}
~~~

The environment variable `access_token` will update automatically.

---

## Running Requests

Once authenticated, you can run:

- **Menu** → GET /menu/  
- **Cart** → GET/POST/DELETE  
- **Orders** → GET/POST/PATCH  
- **Ratings** → POST /ratings/  

Each request is preconfigured with the correct URL and headers.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|--------|------|
| 401 Unauthorized | Missing/expired token | Re-run login request |
| 403 Forbidden | Wrong role | Log in as correct test user |
| 400 Bad Request | Invalid JSON | Check request body |

---

## Tips

- Use **Collections → Run** to batch‑test endpoints  
- Duplicate requests to test variations  
- Use the **Console** (View → Show Postman Console) to debug  




