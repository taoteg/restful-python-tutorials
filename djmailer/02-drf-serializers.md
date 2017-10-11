
# Django REST Framework: Serializers

_Written by masnunon May 13, 2017_

**(This post is a part of a tutorial series on [Building REST APIs in Django](http://polyglot.ninja/django-building-rest-apis/))**

In our last blog post, Getting started with Django REST Framework, we saw how we could use the APIView and accept inputs from users using `request.data`. In our example, we dealt with string, so it was pretty straightforward. But consider the case of `age` or `account_balance` – one has to be integer, the other has to be float / decimal. How do we properly validate the incoming data?

We can manually check every input field and send an error if the field type doesn’t match. But soon we’re going to have a problem at our hand – when the number of inputs will grow, we can’t just keep doing this kind of manual validation. In Django, we would probably use Django Forms for validation. Does DRF provide us with something similar? Yes, it does. The solution to our problem is Serializers.

## What can a Serializer do for us?

Have you ever tried JSON serializing a Django model? Or a queryset? You can’t directly because they are not JSON serializable. So what do we do instead? We convert them to Python’s native data structures which could be serialized into JSON. We can serialize querysets into lists and model instances to dictionaries. But doing that by hand is cumbersome.

On the other hand, we saw how we can get incoming data from `request.data` – we get this data as key value pairs. We can’t just store them in database directly – we have to transform them into Django’s data structures like models and querysets. Doing that by hand is also cumbersome.

Serializers can help us with that. It can serialize complex types into Python natives types and then again deserialize native types into those complex types. Besides that, it also does basic validation based on the serializer field types. If a field is defined as an integer field, it will raise an error if we pass a string to that field. If we need more advanced validation rules, we can plug in the built in **Validators** or even write our own. Let’s see code examples to understand the use case better.

## Defining a Serializer

Create a file named `serializers.py` inside the `api` app directory. Put the following codes into it.

```
from rest_framework import serializers


class HelloWorldSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=6)
    age = serializers.IntegerField(required=False, min_value=10, default=10)
```

We’re creating a `HelloWorldSerializer` which extends `serializers.Serializer`. We’re defining two fields on this serializer –

    * `name` is a `CharField` so it accepts string. It has a `max_length` of 6.
    * `age` is an optional integer field. The value must be at least 10 if provided. If not provided, default value will be 10.

With this serializer setup, let’s modify our view to use it.

```
from rest_framework import serializers


class HelloWorldSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=6)
    age = serializers.IntegerField(required=False, min_value=10, default=10)
```

We pass the `request.data` as the `data` parameter to `HelloWorldSerializer` so it can read all the request data and parse them. Then we check if the serializer is valid. If you have used Django Forms, this will feel very similar. If the serializer is valid, that means we have a valid set of data available. So we can take the value of name and age and show a pretty message. On the other hand, if the serializer is not valid, we can pass the `serializer.errors` back to the client, which will contain elaborate error messages.

Let’s try out the API to see what happens. Let’s first send an empty request:

```
$ curl -H "Content-Type: application/json" -X POST http://localhost:8000/api/hello

{"errors":{"name":["This field is required."]}}
```

The errors say the `name` field is required. Of course it is! Let’s pass the name.

```
$ curl -H "Content-Type: application/json" -X POST -d '{"name": "masnun"}' http://localhost:8000/api/hello

{"message":"Hello masnun, you're 10 years old"}
```

We just passed the name but didn’t pass the age. Since it is not required and has a default value set, we get the default value. But what if we set a low value?

```
$ curl -H "Content-Type: application/json" -X POST -d '{"name": "masnun", "age": '8'}' http://localhost:8000/api/hello

{"errors":{"age":["Ensure this value is greater than or equal to 10."]}}
```

So we passed 8 and it’s not happy about that. Please note we passed the 8 as a string but DRF doesn’t mind as long as it can convert it to an integer successfully. What if we pass a value that is no number?

```
$ curl -H "Content-Type: application/json" -X POST -d '{"name": "masnun", "age": "ten"}' http://localhost:8000/api/hello

{"errors":{"age":["A valid integer is required."]}}
```

That works too! Cool, okay then let’s give it a rest and pass a valid value.

```
$ curl -H "Content-Type: application/json" -X POST -d '{"name": "masnun", "age": "ten"}' http://localhost:8000/api/hello

{"errors":{"age":["A valid integer is required."]}}
```

## Serializer with Model

How does Serializers help us in working with models? To understand that, let’s first create one model.

### Creating the Subscriber Model

Open `api/models.py` and add the Subscriber model like this:

```
class Subscriber(models.Model):
    name = models.CharField("Name", max_length=50)
    age = models.IntegerField("Age")
    email = models.EmailField("Email")
```

Now create and run the migration.

```
python manage.py makemigrations
python manage.py migrate
```

That should setup the table for our new model.

### Update The Serializer

We added an email field to our model, also the max length for name is now 50 chars. Let’s update our serializer to match these constraints. Also rename it as `SubscriberSerializer`.

```
from rest_framework import serializers


class SubscriberSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    email = serializers.EmailField()
```

### Update The View

And now let’s refactor our view.

```
from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberView(APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})

    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            subscriber_instance = Subscriber.objects.create(**serializer.data)
            return Response({"message": "Created subscriber {}".format(subscriber_instance.id)})
        else:
            return Response({"errors": serializer.errors})
```

The code is very simple and straightforward. If the serializer validation succeeds, we create a new subscriber out of the validated data.

### Update URLConf

Let’s update the urls.py to update our url end point.

```
url(r'^subscriber', SubscriberView.as_view(), name="subscriber")
```

Now let’s try it out. We will post the following JSON using curl or postman:

```
{"name": "Abu Ashraf Masnun", "email": "masnun@polyglot.ninja", "age": 29}
```

And we will get back the following response:

```
{
  "message": "Created subscriber 1"
}
```

With the serializer, we needed so much less codes. And we did it in a very clean way.

### List All Subscribers

According to the [REST Best Practices](http://polyglot.ninja/rest-api-best-practices-python-flask-tutorial/), the `GET` call to a resource route (`/api/subscriber`) should return a list of all the items (subscribers). So let’s refactor the `get` method to return the subscribers list.

```
def get(self, request):
        all_subscribers = Subscriber.objects.all()
        serialized_subscribers = SubscriberSerializer(all_subscribers, many=True)
        return Response(serialized_subscribers.data)
```

We are fetching all subscribers and then passing the queryset to the serializer constructor. Since we’re passing a query set (not just a single model instance rather a list of model instances), we need to set  `many=True` . Also note, we don’t need to call `is_valid` – the data is coming from database, they’re already valid. In fact, we can’t call `is_valid` unless we’re passing some value to the `data` parameter (`SubscriberSerializer(data=request.data)`). When we pass queryset or model, the data is automatically available as `serializer.data`.

## What’s Next?

We have so far learned how to use APIView and Serializer to build beautiful APIs with clean code. But we still have some duplication of efforts, for example when we had to define fields on both the model and the serializer. Also, we have to implement both collection and element resources. So that’s like 5 method implementation. Wouldn’t it be great if, by some mechanism we could make things simpler, shorter and cleaner?

We’ll see, in our next blog post 🙂 Please subscribe to our mailing list for email updates. Also if you liked the content, please don’t forget to share with your friends!
