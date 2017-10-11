
# Django REST Framework: ViewSet, ModelViewSet and Router

_Written by masnunon May 14, 2017_

**(This post is a part of a tutorial series on [Building REST APIs in Django](http://polyglot.ninja/django-building-rest-apis/))**

In our last blog post on ModelSerializer and Generic Views, we demonstrated how we can use the generic views along with ModelSerializer classes to rapidly develop our REST APIs. In this post, we will discuss about ViewSet and ModelViewset and see how they can speed up building APIs even further. At the same time we will take a look at the concepts of Routers which allow us to manage our api routes in a cleaner fashion.

## Understanding ViewSet

So far we have learned how we can use the generic views. We can now use them to create the two kinds of resources – “collections” and “elements”. It works very well but we need to write at least two different classes to handle them properly. But if we think about it, both resources focus on the same entity, the same model – “Subscriber”. Wouldn’t it make more sense if we could have all the actions related to a Subscriber in a single class? Wouldn’t that be more convenient if we can put all the Subscriber related logic in a single place?

`ViewSets` come to the rescue. A `ViewSet` is, as the name suggests, a class that provides the functionality of a set of views which are closely related. It’s one class but provides a set of views. We can handle both “collection” and “element” type of resources from the same class. And not just those, we can add even other related actions.

Since a `ViewSet` handles both type of resources, we can no longer think in terms of the http verbs. Because both `/api/subscriber` and `/api/subscriber/1` can respond to  `GET` requests and should produce different types of response. So we can no longer work with the `get`, `post`, `put` etc methods. We need to think more along the actions we can take on the entity (`Subscriber`) as a whole. A `ViewSet` works with these methods instead:

    * `list` – list all elements, serves `GET` to `/api/subscriber`
    * `create` – create a new element, serves `POST` to `/api/subscriber`
    * `retrieve` – retrieves one element, serves `GET` to `/api/subscriber/1`
    * `update` and `partial_update` – updates single element, handles `PUT`/`PATCH` to `/api/subscriber/1`
    * `destroy` – deletes single element, handles `DELETE` to `/api/subscriber/1`

Instead of our old `get` and `post` methods in separate classes, we can now define these methods in one single class and be done with it. But with general `ViewSet`, we have to provide logic / code for these views. That would require more time and efforts. What if, we could generate these methods from our models / querysets? Well, we can! 😀

## The ModelViewSet

The ModelViewSet would only ask for the serializer class and the queryset. And then it will provide all the functionality of the different ViewSet methods. Let’s see the example:

```
from rest_framework.viewsets import ModelViewSet

from .serializers import SubscriberSerializer
from .models import Subscriber


class SubscriberViewSet(ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
```

Our `SubscriberViewSet` now extends the `ModelViewSet` and we provided the `queryset` and the `serializer_class`. Done. Really!

But there’s one slight problem, the `ViewSet` and `ModelViewSet` both handle at least two distincts url paths – `/api/subscriber` (the collection path) and `/api/subscriber/1` – the elements path. How do we tell Django’s URLConf to route requests to both urls to our single `ViewSet`? Well, we have to declare those paths ourselves. We can use the `as_view` to both paths, defining which http verb should be routed to which methods:

```
SubscriberViewSet.as_view({'get': 'list', 'post':'create'}) # For: /api/subscriber
SubscriberViewSet.as_view({'get': 'retrieve', 'put':'update'}) # For: /api/subscriber/1
```

Or we can simply use a Router.

## Using Routers

A `Router` instance let’s us `register` our `ViewSet` to it and then we can just add the `router.urls` to our `urlpatterns`. It will keep track of the view sets we register and the `urls` property will generate all the url patterns required for those view sets to work.  Let’s add our newly created `SubscriberViewSet` to a router and see for ourselves. Open the `api/urls.py` file and create the router there and register the viewset.

```
from rest_framework.routers import SimpleRouter

from .views import SubscriberViewSet

router = SimpleRouter()
router.register("subscribers", SubscriberViewSet)

urlpatterns = router.urls
```

That’s all that is required. Now try visiting – http://localhost:8000/api/subscribers or http://localhost:8000/api/subscribers/1 – it all works.

Fantastic, so we just generated a full RESTful API from a model with a surprisingly short amount of code! Isn’t that wonderful? Just don’t trust my words, go and look at your `SubscriberViewSet` or the `SubscriberSerializer` or the above defined router.

With the help of `ModelSerializer`, `ModelViewSet` and a router instance, we can build elegant CRUD APIs from our Django models insanely fast. At the same time, if we need, we can just override one of those methods (list, retrieve, create etc) to alter the default behavior with our own.

## What’s Next?

We have crafted a nice, functional REST API. The next stop would be securing it. In our next post, we will be discussing Authentication and Permissions.

In the mean time, I would request you to subscribe to the mailing list so I can keep you posted about new exciting contents on this site. If you liked the post, please do share with your friends!
