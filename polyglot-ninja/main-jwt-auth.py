"""
Starting point for minimal Flask API.
"""

# Import package dependencies.
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity

# Create a new Flask App.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

# Wrap the App in an API.
api = Api(app, prefix="/api/v1")

# Simple password login for testing.
USER_DATA = {
    "ttg":"password"
}

#
class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id


# JWT verify method.
def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=667)


# JWT identity method.
def identity(payload):
    user_id = payload['identity']
    return {"user_id":user_id}


# Instantiate JWT Auth.
jwt = JWT(app, verify, identity)


# Create API Resources by extending Resource.

# JWT Auth example endpoint.
class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        # return {"meaning_of_life":42}
        # return {"meaning_of_life":42}, 204    # Error code causes silent response.
        return dict(current_identity)


# Define Routes to the API Resources.
api.add_resource(PrivateResource, '/private')

# Run the Flask API App.
if __name__ == '__main__':
    app.run(debug=True)
