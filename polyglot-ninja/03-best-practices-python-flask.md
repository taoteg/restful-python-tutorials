# REST API Best Practices: Python & Flask Tutorial

_Written by MASNUNon MAY 6, 2017_

In our last post about REST APIs, we have learned the basics of how REST APIs function. In this post, we would see how we can develop our own REST APIs. We would use Python and Flask for that. If you are new to Python, we have you covered with our Python: Learning Resources and Guidelines post.

Python / Flask code is pretty simple and easy to read / understand. So if you just want to grasp the best practices of REST API design but lack Python skills, don’t worry, you will understand most of it. However, I would recommend you try out the codes hands on. Writing codes by hand is a very effective learning method. We learn more by doing than we learn by reading or watching.

## Installing Flask and Flask-RESTful

We will be using the Flask framework along with Flask-RESTful. Flask-RESTful is an excellent package that makes building REST APIs with Flask both easy and pleasant. Before we can start building our app, we first need to install these packages.

```
pip install flask
pip install flask-restful
```

Once we have the necessary packages installed, we can start thinking about our API design.

## RESTful Mailing List

You see, I just recently started this [Polyglot.Ninja()](http://polyglot.ninja/hello-polyglot-ninja/) website and I am getting some readers to my site. Some of my readers have shown very keen interest to receive regular updates from this blog. To keep them posted, I have been thinking about building a mailing list where people can subscribe with their email address. These addresses get stored in a database and then when I have new posts to share, I email them. Can we build this mailing list “service” as a REST API?

The way I imagine it – we will have a “subscribers” collection with many subscriber. Each subscriber will provide us with their full name and email address. We should be able to add new subscriber, update them, delete them, list them and get individual data. Sounds simple? Let’s do this!

## Choosing a sensible URL

We have decided to build our awesome mailing list REST API. For development and testing purposes, we will run the app on my local machine. So the base URL would be http://localhost:5000. This part will change when we deploy the API on a production server. So we probably don’t need to worry about it.

However, for API, the url path should make sense. It should clearly state it’s intent. A good choice would be something like `/api/` as the root url of the API. And then we can add the resources, so for subscribers, it can be `/api/subscribers`. Please note that it’s both acceptable to have the resource part singular (ie. `/api/subscriber`) or plural (`/api/subscribers`). However, most of the people I have talked to and the articles I have read, more people like the plural form.

## API Versioning: Header vs URL

We need to think about the future of the API before hand. This is our first iteration. In the future, we might want to introduce newer changes. Some of those changes can be breaking changes. If people are still using some of the older features which you can’t break while pushing new changes, it’s time you thought about versioning your API. It is always best practice to version your API from the beginning.

The first version of the api can be called `v1`. Now there are two common method of versioning APIs – 1) Passing a header that specifies the desired version of the API  2) Put the version info directly in the URL. There are arguments and counter arguments for both approaches. However, versioning using url is easier and more often seen in common public APIs.

So we accommodate the version info in our url and we make it – `/api/v1/subscribers`. Like discussed in our previous REST article, we will have two types of resources here – “subscriber collection” (ie. `/subscribers`) and “individual subscriber” elements (ie. `/subscribers/17`).  With the design decided upon and a bigger picture in our head, let’s get to writing some codes.

RESTful Hello World

Before we start writing our actual logic, let’s first get a hello world app running. This will make sure that we have got everything setup properly. If we head over to the [Flask-RESTful Quickstart page](http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html), we can easily obtain a hello world code sample from there.

```
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
```

Let’s save this code in a file named `main.py` and run it like this:

`$ python main.py`

If the code runs successfully, our app will launch a web server here – http://127.0.0.1:5000/. Let’s break down the code a bit:

* We import the necessary modules (Flask and Flask-RESTful stuff).
* Then we create a new `Flask` app and then wrap it in `Api`.
* Afterwards, we declare our `HelloWorld` resource which extends `Resource`.
* On our resource, we define what the `get` http verb will do.
* Add the resource to our API.
* Finally run the app.

What happens here, when we write our `Resource`s, Flask-RESTful generates the routes and the view handlers necessary to represent the resource over RESTful HTTP. Now let’s see, if we visit the url, do we get the message we set?

If we visit the url, we would see the expected response:

```
{
    "hello": "world"
}
```

## Trying out REST APIs

While we develop our api, it is essential that we can try out / test the API to make sure it’s working as expected. We need a way to call our api and inspect the output. If you’re a command line ninja, you would probably love to use curl. Try this on your terminal:

```
$ curl -X GET http://localhost:5000
{
    "hello": "world"
}
```

This would send a GET request to the URL and curl would print out the response on the terminal. It is a very versatile tool and can do a lot of amazing things. If you would like to use curl on a regular basis, you may want to dive deeper into the options / features / use cases. These can help you:

* [curl manual](https://curl.haxx.se/docs/manual.html)
* [automating http jobs with curl](https://curl.haxx.se/docs/httpscripting.html)
* [curl unix manpage](https://curl.haxx.se/docs/manpage.html)

However, if you like command line but want a friendlier and easier command line tool, definitely look at [httpie](https://httpie.org/).

httpie vs curl (img)
httpie vs curl command (caption)

Now what if you’re not a CLI person? And we can agree that sometimes GUI can be much more productive to use. Don’t worry, [Postman](https://www.getpostman.com/) is a great app!

If you are developing and testing a REST API, Postman is a must have app!

postman interface (img)
Our newly created API in Postman (caption)

## Back to Business

We now have a basic skeleton ready and we know how to test our API. Let’s start writing our mailing list logic. Let’s first layout our resources with some sample data. For this example, we shall not bother about persisting the data to some database. We will store the data in memory. Let’s use a list as our subscriber data source for now.

```
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

users = [
    {"email": "masnun@gmail.com", "name": "Masnun", "id": 1}
]


class SubscriberCollection(Resource):
    def get(self):
        return {"msg": "All subscribers "}
    def post(self):
        return {"msg": "We will create new subscribers here"}


class Subscriber(Resource):
    def get(self, id):
        return {"msg": "Details about user id {}".format(id)}
    def put(self, id):
        return {"msg": "Update user id {}".format(id)}
    def delete(self, id):
        return {"msg": "Delete user id {}".format(id)}


api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
```

_**What changes are notable here?**_

* Note we added a `prefix` to the `Api` for versioning reason. All our urls will be prefixed by  `/api/v1`.
* We created a list named `users` to store the subscribers.
* We created two resources – `SubscriberCollection` and `Subscriber`.
* Defined the relevant http method handlers. For now the response just describes the intended purpose of that method.
* We add both resources to our api. Note how we added the `id` parameter to the url. This `id` is available to all the methods defined on `Subscriber`.

Fire up the local development server and try out the API. Works fine? Let’s move on!

## Parsing Request Data

We have to accept, validate and process user data. In our cases, they would be the subscriber information. Each subscriber would have an email address, a full name and ID. If we used a database, this ID would have been auto generated. Since we are not using a database, we would accept this as part of the incoming request.

For processing request data, the `RequestParser` can be very helpful. We will use it in our `POST` calls to `/api/subscribers/` to validate incoming data and store the subscriber if the data is valid. Here’s the updated code so far:

```
from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

users = [
    {"email": "masnun@gmail.com", "name": "Masnun", "id": 1}
]

subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")


class SubscriberCollection(Resource):
    def get(self):
        return users
    def post(self):
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}


class Subscriber(Resource):
    def get(self, id):
        return {"msg": "Details about user id {}".format(id)}
    def put(self, id):
        return {"msg": "Update user id {}".format(id)}
    def delete(self, id):
        return {"msg": "Delete user id {}".format(id)}


api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
```

_**Here we have made two key changes:**_

* We created a new instance of `RequestParser` and added `arguments` so it knows which fields to accept and how to validate those.
* We added the request parsing code in the `post` method. If the request is valid, it will return the validated data. If the data is not valid, we don’t have to worry about it, the error message will be sent to the user.

## Testing the request parser

If we try to pass invalid data, we will get error messages. For example, if we request without any data, we will get something like this:
```
{
  "message": {
    "email": "Missing required parameter in the JSON body or the post body or the query string",
    "id": "Please enter valid integer as ID",
    "name": "Name has to be valid string"
  }
}
```

But if we pass valid data, everything works fine. Here’s an example of valid data:
```
{"email": "john@polyglot.ninja", "name": "John Smith", "id": 3}
```

This will get us the following response:
```
{
  "msg": "Subscriber added",
  "subscriber_data": {
    "email": "john@polyglot.ninja",
    "id": 3,
    "name": "John Smith"
  }
}
```

Cool, now we know how to validate user data 🙂

**Please remember – never trust user input. Always validate and sanitize user data to avoid security risks.**

Next, we need to implement the user level updates.

## Subscriber Views

We went ahead and completed the code for the rest of the methods. The updated code now looks like this:
```
from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
api = Api(app, prefix="/api/v1")

users = [
    {"email": "masnun@gmail.com", "name": "Masnun", "id": 1}
]


def get_user_by_id(user_id):
    for x in users:
        if x.get("id") == int(user_id):
            return x


subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")


class SubscriberCollection(Resource):
    def get(self):
        return users
    def post(self):
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}


class Subscriber(Resource):
    def get(self, id):
        user = get_user_by_id(id)
        if not user:
            return {"error": "User not found"}
        return user
    def put(self, id):
        args = subscriber_request_parser.parse_args()
        user = get_user_by_id(id)
        if user:
            users.remove(user)
            users.append(args)
        return args
    def delete(self, id):
        user = get_user_by_id(id)
        if user:
            users.remove(user)
        return {"message": "Deleted"}


api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
```

_**What did we do?**_

* We added a helper function to find users from the list by it’s id
* The update view works – we can update the user data. In our case we’re deleting the data and adding the new data. In real life, we would use `UPDATE` on the database.
* Delete method works fine!

Feel free to go ahead and test the endpoints!

## HTTP Status Codes

Our mailing list is functional now. It works! We have made good progress so far. But there’s something very important that we haven’t done yet. Our API doesn’t use proper http status codes. When we send response back to the client, we should also give it a status code. This code would help the client better interpret the results.

Have you ever visited a website and saw “404 Not found” error? Well, 404 is the status code, that means the document / resource you were looking for is not available. Saw any “500 Internal Server Error” lately? Now you know what that 500 means.

We can see the complete list of http status codes here: [https://httpstatuses.com/](https://httpstatuses.com/).

Also depending on whether you’re a cat person or a dog enthusiast, these websites can explain things better:

* [https://http.cat/](https://http.cat/)
* [https://httpstatusdogs.com/](https://httpstatusdogs.com/)

So let’s fix our code and start sending appropriate codes. We can return an optional status code from our views. So when we add a new subscriber, we can send  201 Created like this:
```
return {"msg": "Subscriber added", "subscriber_data": args}, 201
```

And when we delete the user, we can send 204.
```
return None, 204
```

## What’s next?

We have made decent progress today. We have designed and implemented a very basic API. We chose a sensible url, considered API versioning, did input validation and sent appropriate http status codes. We have done good. But what we have seen here is a very simple implementation. There are a lot of scope of improvements here. For example, our API is still open to public, there is no authentication enabled. So anyone with malicious intentions can flood / spam our mailing list database. We need to secure the API in that regard. We also don’t have a home page that uses HATEOAS to guide the clients. We don’t yet have documentation – always remember, the documentation is very important. We developers often don’t feel like writing documentation but well written documentation helps the consumers of your API consume it better and with ease. So do provide excellent docs!

I don’t know when – but in our next post on REST APIs, we shall explore more into the wonderful world of API development. And may be we shall also talk about some micro services? If you would like to know when I post those contents, do subscribe to the mailing list. You can find a subscription form on the sidebar.

And if you liked the post, do share with your friends 🙂
