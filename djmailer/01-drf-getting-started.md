
# Django REST Framework: Getting Started

_Written by masnunon May 13, 2017_

**(This post is a part of a tutorial series on [Building REST APIs in Django](http://polyglot.ninja/django-building-rest-apis/))**

In our last post about Building APIs in Django, we explained why using Django REST Framework would be a good idea. In this post, we will start writing our APIs using this awesome framework. DRF itself works on top of Django and provides many useful functionality that can help with rapid API development.

## Installing Django REST Framework

We have to install DRF first. We can install it using pip as usual.

```
pip install djangorestframework
```

Once the installation succeeds, add `rest_framework` to the `INSTALLED_APPS` list in `settings.py`.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'api'
]
```

Now we are ready to start building our awesome APIs!

## Using APIView

`APIView` class is quite similar to Django’s `View` class except it is more REST-y! The `APIView` class can be considered as quite similar to the Flask Resource class from our [Flask Tutorial](http://polyglot.ninja/rest-api-best-practices-python-flask-tutorial/). An `APIView` has methods for the HTTP verbs. We can implement our own methods to handle those requests the way we want.

Let’s modify the function we wrote in our first post to use `APIView` instead.

```
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})
```

We have done two things –

    * Our `HelloWorldView` extends `APIView` and overrides the `get` method. So now DRF knows how to handle a `GET` request to the API.
    * We return an instance of the `Response` class. DRF will do the content negotiation for us and it will render the response in the correct format. We don’t have to worry about rendering JSON / XML any more.

Since we are now using a class based view, let’s update the urlconf and make the following change:

```
url(r'^hello', HelloWorldView.as_view(), name="hello_world")
```

That’s all the change that is necessary – we import the class based view and call the `as_view` method on it to return a view that Django can deal with. Under the hood, the `as_view` class method works as an entry point for the request. The class inspects the request and properly dispatches to the `get`, `post`, `put` etc methods to process the request. It then takes the result and sends back like a normal function based view would do. In short, the `as_view` method kind of works as a bridge between the class based view and the function based views commonly used with Django.

### The Web Browsable API

If you visit `http://localhost:8000/api/hello` you will now see a nice html view with our json response displayed along with other useful information (response headers). This html view is an excellent feature of DRF – it’s called the web browsable API. The APIs we create, DRF automagically generates a web view for us from where we can interact with our API, testing / debugging things. No need for swagger or any other external clients for testing. Awesome, no?

### Function Based APIView

We can also use a function based form of APIView where we write a function and wrap it using the `api_view` decorator. An example would look like this:

```
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def hello_world(request):
    if request.method == "GET":
        return Response({"message": "Hello World!"})

    else:
        name = request.data.get("name")
        if not name:
            return Response({"error": "No name passed"})
        return Response({"message": "Hello {}!".format(name)})
```

And in the urls.py, the entry will look like this:

```
url(r'^hello', hello_world, name="hello_world")
```

I mostly use function based views when things are really simple and I have to handle just one type of request (say, `POST` or `GET`). But in case I have to handle multiple type of requests, I will then have to check `request.method` to determine the type and handle accordingly. I find the class based view cleaner and well organized than writing a bunch of if else blocks.

You can read more about the function based APIView in the docs.

## Accepting Input

We have seen how to write a simple end point to say “hello world!” – that is great. But now we must learn how we can handle inputs from our user. For this demonstration, on our `/api/hello` endpoint, we would accept a `name` in a `POST` request. If the name is passed, we will show a customized greeting. Let’s get to work!

```
class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"error": "No name passed"})
        return Response({"message": "Hello {}!".format(name)})
```

We have added a `post` method that should handle the `POST` requests. Instead of `request.POST`, we would use `request.data` which works across `POST`, `PUT`, `PATCH`  – all other methods too. If the name is not passed we send error message. Otherwise we send a hello world message.

With that code written, let’s try it out –

```
$ curl -H "Content-Type: application/json" -X POST -d '{"name":"masnun"}' http://localhost:8000/api/hello

{"message":"Hello masnun!"}
```


Aha, things worked as expected! Cool! What if we don’t pass the name?

```
$ curl -H "Content-Type: application/json" -X POST  http://localhost:8000/api/hello

{"error":"No name passed"}
```

It works exactly like we wanted it to! Fantastic!

## What’s next?

In this post, we saw how the APIView works and how we can accept inputs and send responses for different http verbs. In the next post, we will discuss about serializers and how they can be useful.

If you would like to get notified when we post new content, please subscribe to our mailing list. We will email you when there’s something new here 🙂
