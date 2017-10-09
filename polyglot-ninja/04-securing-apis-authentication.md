# Securing REST APIs: Basic HTTP Authentication with Python / Flask

_Written by MASNUNon MAY 10, 2017_

In our last tutorial on REST API Best Practices, we designed and implemented a very simple RESTful mailing list API. However our API (and the data) was open to public, anyone could read / add / delete subscribers from our mailing list. In serious projects, we definitely do not want that to happen. In this post, we will discuss how we can use http basic auth to authenticate our users and secure our APIs.

PS: If you are new to REST APIs, please check out REST APIs: Concepts and Applications to understand the fundamentals.

## Setup API and Private Resource

Before we can move on to authentication, we first need to create some resources which we want to secure. For demonstration purposes, we will keep things simple. We will have a very simple endpoint like below:
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

If we launch the server and access the endpoint, we will get the expected output:
```
$ curl -X GET http://localhost:5000/api/v1/private
{
    "meaning_of_life": 42
}
```

Our API is for now public. Anyone can access it. Let’s secure it so it’s no longer publicly accessible.

## Basic HTTP Authentication

The idea of Basic HTTP Authentication is pretty simple. When we request a resource, the server sends back a header that looks something like this: WWW-Authenticate →Basic realm=”Authentication Required”. Generally when we try to access such resources from a browser, the browser shows us a prompt to enter username and password. The browser then base64 encodes the data and sends back an Authorization header. The server parses the data and verifies the user. If the user is legit, the resource is accessible, otherwise we are not granted permission to access it.

While using a REST Client, we would very often need to pass the credentials before hand, while we make the request. For example, if we’re using `curl`, we need to pass the `--user` option while running the command.

Basic HTTP Authentication is a very old method but quite easy to setup. [Flask HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth) is a nice extension that would help us with that.

Install Dependencies

Before we can start writing codes, we need to have the necessary packages installed. We can install the package using `pip`: `$ pip install Flask-HTTPAuth`

Once the package is installed, we can use it to add authentication to our API endpoints.

## Require Login

We will import the `HTTPBasicAuth` class and create a new instance named `auth`. It’s important to note that name because we will be using methods on this auth instance as decorators for various purposes.  For example, we will use the `@auth.login_required` decorator to make sure only logged in users can access the resource.

In our resource, we added the above mentioned decorator to our `get` method. So if anyone wants to `GET` that resource, s/he needs to login first. The code looks like this:
```
from flask import Flask
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()


class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        return {"meaning_of_life": 42}


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
```

If we try to access the resource without logging in, we will get an error telling us we’re not authorized. Let’s send a quick request using `curl`.
```
$ curl -X GET http://localhost:5000/api/v1/private
Unauthorized Access
```

So it worked. Our API endpoint is now no longer public. We need to login before we can access it. And from the API developer’s perspective, we need to let the users login before they can access our API. How do we do that?

## Handling User Logins

We would generally store our users in a database. Well, a secured database. And of course, we would **never store user password in plain text**. But for this tutorial, we would store the user credentials in a dictionary. The password will be in plain text.

Flask HTTP Auth will handle the authentication process for us. We just need to tell it how to verify the user with his/her username and password. The `@auth.verify_password` decorator can be used to register a function that will receive the username and password. This function will verify if the credentials are correct and based on it’s return value, HTTP Auth extension will handle the user auth.

In the following code snippet, we register the `verify` function as the callback for verifying user credentials.  When the user passes the credentials, this function will be called. If the function returns `True`, the user will be accepted as authorized. If it returns `False`, the user will be rejected. We have kept our data in the `USER_DATA` dictionary.
```
USER_DATA = {
    "admin": "SuperSecretPwd"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password
```

Once we have added the above code, we can now test if the auth works.
```
$ curl -X GET http://localhost:5000/api/v1/private --user admin:SuperSecretPwd
{
    "meaning_of_life": 42
}
```

But if we omit the auth credentials, does it work?
```
$ curl -X GET http://localhost:5000/api/v1/private
Unauthorized Access
```

It doesn’t work without the login. Perfect! We now have a secured API endpoint that uses basic http auth. But in all seriousness, it’s **not recommended**.  That’s right, do not use it in the public internet. It’s perhaps okay to use inside a private network. Why? Please read [this thread](https://security.stackexchange.com/questions/988/is-basic-auth-secure-if-done-over-https).

## Wrapping Up

With the changes made, here’s the full code for this tutorial:
``
from flask import Flask
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "SuperSecretPwd"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        return {"meaning_of_life": 42}


api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
    app.run(debug=True)
```

As discussed in the last section, it’s not recommended to use basic http authentication in open / public systems. However, it is good to know how http basic auth works and it’s simplicity makes beginners grasp the concept of authentication / API security quite easily.

You might be wondering – “If we don’t use http auth, then what do we use instead to secure our REST APIs?”. In our next tutorial on REST APIs, we would demonstrating how we can use JSON Web Tokens aka JWT to secure our APIs. Can’t wait for that long? Go ahead and read the introduction.

And don’t forget to subscribe to the mailing list so when I write the next post, you get a notification!
