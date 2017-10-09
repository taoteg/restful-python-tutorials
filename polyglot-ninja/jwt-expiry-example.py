import jwt
import datetime
import time

payload = {
    "uid": 23,
    "name":"mungbean",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=2)
}

SECRET_KEY = "SUPERSECRET"

token = jwt.encode(payload=payload, key=SECRET_KEY)

print("Generated Token: {}".format(token.decode()))

time.sleep(10)  # Wait 10 seconds so the token expires.

decoded_payload = jwt.decode(jwt=token, key=SECRET_KEY)

print(decoded_payload)
