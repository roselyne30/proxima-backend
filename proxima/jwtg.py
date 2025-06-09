import jwt
import datetime

# Your secret key (make sure it's the same one you're using in Flask)
secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5b3VyX3VzZXJfaWRfaGVyZSIsImV4cCI6MTc0OTE2NTM0MX0.fyh6NbP2UYS3zAgVow4a4EokQZMrdXKKAj4klN0JBIY'

# Payload data (claims)
payload = {
    'sub': 'your_user_id_here',  # Substitute with the user id you want to assign
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiration time (optional)
}

# Generate the JWT
token = jwt.encode(payload, secret_key, algorithm='HS256')

print(f"JWT Token: {token}")
