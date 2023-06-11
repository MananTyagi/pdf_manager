from jose import jwt
from datetime import datetime, timedelta

def generate_jwt_token(user_name):
    # Set the expiration time (e.g., 1 hour from the current time)
    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    
    # Create the payload with the user ID and expiration time
    payload = {
        'user_name': user_name,
        'exp': expiration_time
    }
    
    # Generate the JWT token with a secret key
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    
    return token

def verify_jwt_token(token):
    try:
        # Verify the token's signature and expiration time
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        
        # Extract the user ID and expiration time from the payload
        user_name = payload['user_name']
        expiration_time = payload['exp']
        
        # Check if the token has expired
        if datetime.utcnow() > datetime.fromtimestamp(expiration_time):
            raise jwt.ExpiredSignatureError('Token has expired')
        
        return user_name
    except jwt.DecodeError:
        # Handle invalid token signature
        raise jwt.InvalidTokenError('Invalid token')
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise jwt.ExpiredSignatureError('Token has expired')