# JWT Authentication with Python and Flask

_Written by MASNUNon MAY 12, 2017_

In our blog post about HTTP Authentication, we promised we would next cover JSON Web Tokens aka JWT based authentication. So we wrote a detailed blog post on The Concepts of JWT explaining how the technology works behind the scene. And in this blog post, we would see how we can actually implement it in our REST API. In case you have missed them, we have also explained the basics of REST APIs  along with a Python / Flask tutorial walking through some of the best practices.

## PyJWT or a Flask Extension?

In our last blog post on JWT, we saw code examples based on the PyJWT library. A quick Google search also revealed a couple of Flask specific libraries. What do we use?

We can implement the functionality with PyJWT alright. It will allow us fine grained control. We would be able to customize every aspect of how the authentication process works. On the other hand, if we use Flask extensions, we would need to do less since these libraries or extensions already provide some sort of integrations with Flask itself. Also personally, I tend to choose my framework specific libraries for a task. They reduce the amount of task required to get things going.

In this blog post, we would be using the `Flask-JWT` package.

# Getting Started

Before we can begin, we have to install the package using `pip`.

```
pip install Flask-JWT
```

We also need an API end point that we want to secure. We can refer to the initial code we wrote for our HTTP Auth tutorial.

```
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app, prefix="/api/v1")


class PrivateResource(Resource):
    def get(self):
        return {"meaning_of_life": 42}


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
```

Now we work on securing it 🙂

## Flask JWT Conventions

Flask JWT has the following convention:

* There needs to be two functions – one for authenticating the user, this would be quite similar to the `verify` function we wrote in our last tutorial (http auth tutorial). The second function’s job is to identify user from a token. Let’s call this function `identity`.
* The authentication function must return an object instance that has an attribute named `id`.
* To secure an endpoint, we use the `@jwt_required` decorator.
* An API endpoint is setup at `/auth` that accepts `username` and `password` via JSON payload and returns `access_token` which is the JSON Web Token we can use.
* We must pass the token as part of the `Authorization` header, like – `JWT <token>`.

## Authentication and Identity

First let’s write the function that will authenticate the user. The function will take in username and password and return an object instance that has the `id` attribute. In general, we would use database and the id would be user id. But for this example, we would just create an object with an ID of our choice.

```
USER_DATA = {
    "masnun": "abc123"
}


class User(object):
    def __init__(self, id):
        self.id = id
    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)
```

We are storing the user details in a dictionary like before. We have created User class with `id` attribute so we can fulfil the requirement of having id attribute. In our `verify` function, we compare the username and password and if it matches, we return an `User` instance with the `id` being 123. We will use this function to verify user logins.

Next we need the identity function that will give us user details for a logged in user.

```
def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}
```

The identity function will receive the decoded JWT. An example would be like:

```
{'exp': 1494589408, 'iat': 1494589108, 'nbf': 1494589108, 'identity': 123}
```

Note the `identity` key in the dictionary. It’s the value we set in the `id` attribute of the object returned from the `verify` function. We should load the user details based on this value. But since we are not using the database, we are just constructing a simple dictionary with the user id.

## Securing Endpoint

Now that we have a function to authenticate and another function to identify the user, we can start integrating Flask JWT with our REST API. First the imports:

```
from flask_jwt import JWT, jwt_required
```

Then we construct the jwt instance:

```
jwt = JWT(app, verify, identity)
```

We pass the flask app instance, the authentication function and the identity function to the JWT class.

Then in the resource, we use the `@jwt_required` decorator to enforce authentication.

```
class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return {"meaning_of_life": 42}
```

Please note the `jwt_required` decorator takes a parameter (`realm`) which has a default value of `None`. Since it takes the parameter, we must use the parentheses to call the function first – `@jwt_required()` and **not just `@jwt_required`**. If this doesn’t make sense right away, don’t worry, please do some study on how decorators work in Python and it will come to you 🙂

Here’s the full code:

```
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app, prefix="/api/v1")

USER_DATA = {
    "masnun": "abc123"
}


class User(object):
    def __init__(self, id):
        self.id = id
    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


jwt = JWT(app, verify, identity)


class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return {"meaning_of_life": 42}


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
```

Looks good? Let’s try it out.

## Trying it out

Run the app and try to access the secured resource:

```
$ curl -X GET http://localhost:5000/api/v1/private
{
  "description": "Request does not contain an access token",
  "error": "Authorization Required",
  "status_code": 401
}
```

Makes sense. The endpoint now requires authorization token. But we don’t have one, yet!

Let’s get one – we must send a POST request to `/auth` with a JSON payload containing `username` and `password`. Please note, the api prefix is not used, that is the url for the auth end point is not `/api/v1/auth`. But it is just `/auth`.

```
$ curl -H "Content-Type: application/json" -X POST -d '{"username":"masnun","password":"abc123"}' http://localhost:5000/auth
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQ1OTE4MjcsImlhdCI6MTQ5NDU5MTUyNywibmJmIjoxNDk0NTkxNTI3LCJpZGVudGl0eSI6MTIzfQ.q0p02opL0OxL7EGD7wiLbXbdfP8xQ7rXf7-3Iggqdi4"
}
```

Cool, we got the token. Now let’s use it to access the resource.

```
curl -X GET http://localhost:5000/api/v1/private -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQ1OTE4MjcsImlhdCI6MTQ5NDU5MTUyNywibmJmIjoxNDk0NTkxNTI3LCJpZGVudGl0eSI6MTIzfQ.q0p02opL0OxL7EGD7wiLbXbdfP8xQ7rXf7-3Iggqdi4"
{
    "meaning_of_life": 42
}
```

Whoa, it worked! Amazing, now our JWT authentication is working great!

## Getting the Authenticated User

Once our JWT authentication is functional, we can get the currently authenticated user by using the `current_identity` object.

Let’s add the import:

```
from flask_jwt import JWT, jwt_required, current_identity
```

And then let’s update our resource to return the logged in user identity.

```
class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return dict(current_identity)
```

The `current_identity` object is a LocalProxy instance which can’t be directly JSON serialized. But if we pass it to a `dict()` call, we can get a dictionary representation.

Now let’s try it out:

```
$ curl -X GET http://localhost:5000/api/v1/private -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTQ1OTE4MjcsImlhdCI6MTQ5NDU5MTUyNywibmJmIjoxNDk0NTkxNTI3LCJpZGVudGl0eSI6MTIzfQ.q0p02opL0OxL7EGD7wiLbXbdfP8xQ7rXf7-3Iggqdi4"
{
    "user_id": 123
}
```

As we can see the `current_identity` object returns the exact same data our `identity` function returns because Flask JWT uses that function to load the user identity.

## What’s Next?

Go ahead and implement the same functionality using PyJWT and your own code. You will need to create an endpoint that encodes current user data and returns the access token. Then you will need to intercept the http headers, parse the `Authorization` header and verify the JWT token. It should be a fun and yet excellent learning exercise.
