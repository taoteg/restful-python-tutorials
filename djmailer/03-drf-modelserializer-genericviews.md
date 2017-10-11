# Django REST Framework: ModelSerializer and Generic Views

_Written by masnunon May 14, 2017_

**(This post is a part of a tutorial series on [Building REST APIs in Django](http://polyglot.ninja/django-building-rest-apis/))**

In our last post on Serializers, we learned how to use Serializers with APIViews. In this post we will discuss how ModelSerializer and the Generic views can take things even further.

## Model + Serializer = ModelSerializer

That one line equation is probably enough to explain the concepts of `ModelSerializers`. In our example, we had to define similar fields on both Serializer and the Model class. We had to write codes for the same fields twice. That is 2x the efforts. `ModelSerializers` can help solve that problem. A `ModelSerializer` might remind us of `ModelForm`. The idea is the same. We extend `ModelSerializer` and pass it the model. The serializer inspects the model and knows what fields to use and what their types are.

Let’s refactor our old serializer to be a `ModelSerializer`:

```
from rest_framework import serializers

from .models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"
```

That’s all we need – our new `SubscriberSerializer` now infers the fields from the model (`Subscriber`) we passed to it. We can however choose which fields should be used while serializing / deserializing. In this example we pass the special value “__all__” which means we want to use all fields. But in many cases we would want to selectively use some fields. For example, for Django’s default `User` model, we don’t want to leak the `password` data to public, so we will exclude the `password` field on our User model serializer.

If we try out our API, we would notice everything is working just like before. Except our serializer class is now shorter and more concise. Awesome, right? Let’s move on to our next topic – generic views.

## Generic Views

If you have decent amount of experience with Django, you probably have already come across and used the built in generic views. They provide useful functionality around common database operations. For example, we can use the generic list view and provide it with a queryset and the template, it will do the rest for us.

In the same way, we can pass a queryset and serializer to a `ListAPIView` and it will create the list view for us. Same way we can use `CreateAPIView` to implement the create view. What’s even better, since we’re using class based views, we can use both of them together, cool, no? Let’s refactor old code to use these two classes.

```
from rest_framework.generics import ListAPIView, CreateAPIView

from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberView(ListAPIView, CreateAPIView):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
```

Please note how we no longer need to provide the `get` and `post` methods but the API still works. The generic views just know how to deal with those.

There is actually a `ListCreateAPIView` which is the combination of these two as you can probably understand from the class name. We can just use that one.

```
from rest_framework.generics import ListCreateAPIView

from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberView(ListCreateAPIView):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
```

As you can see this generic view is quite helpful for generating “collection” resources (`/api/subscriber`) easily. There’s also `RetrieveUpdateDestroyAPIView` which we can use to generate “element” resources. As you can guess from the name, they provide `get`, `put`, `patch` and `delete` handler for single items (`/api/subscriber/12`).

Generic views are very handy for quickly generating resources from our models (querysets actually). This allows rapid API development.

## What’s Next?

We have seen how we can very quickly create working REST APIs using model serializers and generic views. Things will be even more amazing when we learn about `ViewSets`, specially `ModelViewSets`. You will have to wait for our next post for those 🙂

In case you didn’t notice, we have a mailing list where you can subscribe to get latest updates. We don’t spam, only contents we post. Also if you enjoyed reading the post and found it informative, shouldn’t you share it with your friends? 😀
