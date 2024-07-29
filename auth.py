# from jwcrypto import jwt, jwk
# from datetime import datetime, timedelta
# import json

# #no key need leave it
# SECRET_KEY = ''

# key = jwk.JWK.from_password(SECRET_KEY)

# def create_token(email):
#     expiration = datetime.utcnow() + timedelta(hours=1)
#     claims = {
#         "email": email,
#         "exp": expiration.isoformat()  
#     }
#     token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
#     token.make_signed_token(key)
#     return token.serialize()

# # def verify_token(token):
# #     try:
# #         verified_token = jwt.JWT(key=key, jwt=token)
# #         claims = json.loads(verified_token.claims)
# #         # Convert the expiration back to a datetime object for comparison
# #         claims['exp'] = datetime.fromisoformat(claims['exp'])
# #         if claims['exp'] < datetime.utcnow():
# #             return None
# #         return claims
# #     except Exception as e:
# #         return None


# # def verify_token(token):
# #     try:
# #         claims = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
# #         return claims
# #     except jwt.ExpiredSignatureError:
# #         print("Token has expired")
# #         return None
# #     except jwt.InvalidTokenError:
# #         print("Invalid token")
# #         return None

# # def verify_token(token):
# #     try:
# #         # Decode and verify the token
# #         verified_token = jwt.JWT(key=key, jwt=token)
# #         claims = json.loads(verified_token.claims)
        
# #         return claims
# #     except Exception as e:
# #         print(f"Token verification error: {e}")
# #         return None
# def verify_token(token):
#     try:
#         verified_token = jwt.JWT(key=key, jwt=token)
#         claims = json.loads(verified_token.claims)
        
#         exp_timestamp = claims.get('exp')
#         if exp_timestamp:
#             current_timestamp = int(time.time())
#             if exp_timestamp < current_timestamp:
#                 print("Token has expired")
#                 return None
        
#         return claims
#     except Exception as e:
#         print(f"Token verification error: {e}")
#         return None
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta
from flask import current_app

def create_token(email):
    expires = timedelta(hours=1)
    access_token = create_access_token(identity=email, expires_delta=expires)
    return access_token


def verify_token(token):
    try:
        claims = decode_token(token)
        email = claims.get('sub')
        if not email:
            raise ValueError("Email not found in token claims")
        return {'email': email}
    except Exception as e:
        current_app.logger.error(f"Token verification error: {e}")
        return None