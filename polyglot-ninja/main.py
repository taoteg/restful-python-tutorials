"""
Starting point for minimal Flask API.
"""

# Import package dependencies.
from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser


# Cra=eate a new Flask App.
app = Flask(__name__)


# Wrap the App in an API.
api = Api(app, prefix="/api/v1")


# Define dummy data for testing API.
users = [
    {"email":"thefirstuser@mail.com", "name":"thefirstuser", "id":1},
    {"email":"theseconduser@mail.com", "name":"theseconduser", "id":2},
    {"email":"thethirduser@mail.com", "name":"thethirduser", "id":3}
]


# Helper Method to get user by ID.
def get_user_by_id(user_id):
    for x in users:
        if x.get("id") == int(user_id):
            return x


# Define RequestParser object.
subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be a valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter a valid integer as ID")


# Create API Resources by extending Resource.
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}, 200


class SubscriberCollection(Resource):
    def get(self):
        # return {"msg":"All Subscribers..."}
        return users, 200

    def post(self):
        # return {"msg":"We will create new subscribers here."}
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg":"Subscriber Added.", "subscriber_data": args}, 201


class Subscriber(Resource):
    def get(self, id):
        # return {"msg":"Details about user id {}".format(id)}
        user = get_user_by_id(id)
        if not user:
            return {"Error":"User not found"}, 404
        return user, 200

    def put(self, id):
        # return {"msg":"Update user id {}".format(id)}
        args = subscriber_request_parser.parse_args()
        user = get_user_by_id(id)
        if user:
            users.remove(user)
            users.append(args)
        return args, 200

    def delete(self, id):
        # return {"msg":"Delete user id {}".format(id)}
        user = get_user_by_id(id)
        if user:
            users.remove(user)
        return {"msg":"User Deleted."}, 204
        # return None, 204


# Define Routes to the API Resources.
api.add_resource(HelloWorld, '/')
api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')


# Run the Flask API App.
if __name__ == '__main__':
    app.run(debug=True)
