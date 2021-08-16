# Demo Django Application with simple JWT

Create sample Django application using simple JWT token support. Which allowas Google Oauth 2.0
login from server side. 

- Need to create login with JWt and Oauth 2.0 with google.
- Create model to track user activities.
- Admin should able to download report in CSV format of user activities.
- Notify team using hook when any login happens.

## Design Aspect
---

I have decided to use simple JWT token for authorisation. 
Created on model UserLoginActivity to track user Activity for login with status of success or fail.

Admin action to download user activities in CSV format from listing view of User Activity model of Admin panel.

One hook to notify team with user's IP when authentication API calls.

Also used swagger for API documentation.

## Usage
---
Run this application using

```python3 manage.py runserver```

For API documentation use :

```http://127.0.0.1:8000/api/docs/```

For login with Google:

```http://127.0.0.1:8000/```

Login using username and password :

```http://127.0.0.1:8000/api/jwtauth/token/```

Register :

```http://127.0.0.1:8000/api/jwtauth/register/```
    
    Example :
    {
        "username": "John",
        "email": "john@gmail.com",
        "password": "123",
        "password2": "123"
    }

Refresh Token :

```http://127.0.0.1:8000/api/jwtauth/refresh/```
