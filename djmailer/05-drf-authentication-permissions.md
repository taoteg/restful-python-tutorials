# Django REST Framework: Authentication and Permissions

_Written by MASNUNon MAY 22, 2017_

**(This post is a part of a tutorial series on Building REST APIs in Django)**

In our last post about ViewSet, ModelViewSet and Router, we saw how easily we can create REST APIs with the awesome Django REST Framework. In this blog post, we would see how we can secure our endpoints with user authentication and permissions. Authentication will help us identify which user is currently logged in and permissions will decide which user(s) can access which resources.

## Authentication

The idea of authentication is pretty simple. When a new incoming request comes, we have to check the request and see if we can identify any user credentials along with it. If you have read the Flask HTTP Auth tutorial or the one about JWT, you might remember how we were checking the authorization header to authenticate our users. We might also receive the user login data via a POST request (form submission) or the user may already be logged in and we can identify using the session data.

We can see that the authentication mechanism can largely vary. Django REST Framework is very flexible in accommodating them. We can give DRF a list of classes, DRF will run the `authenticate` method on those classes. As soon as a class successfully authenticates the user, the return values from the call is set to `request.user` and `request.auth`. If none of the classes manage to authenticate the user, then the user is set to `django.contrib.auth.models.AnonymousUser` .

We can set these classes using the `DEFAULT_AUTHENTICATION_CLASSES` settings under the DRF settings. Here’s an example:

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
```

In the example above we used `BasicAuthentication` and `SessionAuthentication` – two of the built in classes from Django REST Framework. We will look at how they work and we will also check how we can write our own class for our custom authentication.

(PS: Here we set the authentication policy globally, for all views / paths / resources – if we want, we can also use different authentication mechanism for each one, individually but that is usually not done in most cases).

## Basic Authentication

In our example before, we mentioned the `BasicAuthentication` class. This class first checks the http authorization header (`HTTP_AUTHORIZATION` in `request.META` ). If the header contains appropriate string (something like `Basic <Base64 Encoded Login>`), it will decode the string, split the username, password and try to authenticate the user.

Basic Authentication is very simple, easy to setup and might be quite convenient for testing / debugging but I would highly discourage using this method on production.

## Session Authentication

If you have used Django, you already know about session based authentication. In fact, Django itself handles the session based auth and sets the user as part of the `request` object (an instance of `HttpRequest` object. DRF just reads the user data from the request and checks for CSRF. That’s it.

Session Authentication works very well if your users are interacting with your API on the web, perhaps using ajax calls? In such cases, if the user is once logged in, his/her auth is stored in the session and we can depend on those data while making requests from our web app. However, this will not work well if the client doesn’t or can not accept cookies (apps on different domains, mobile or desktop apps, other micro services etc).

## Token Authentication

If you understand JWT, this one will feel similar, except in this case, the token will be just a “token”, no JSON or no signing. The user logs in and gets a token. On subsequent requests, this token must be passed as part of the authorization header.

To use token based auth, we first need to add the `rest_framework.authtoken` app to the `INSTALLED_APPS` list in your `settings.py` file. And then run the migration to create the related tables.

```
python manage.py migrate
```

We also need to add the `TokenAuthentication` class to our DRF auth class list:

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}
```

Now let’s create a view to issue tokens to user.

```
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
```

The code here should be self explanatory. We take username and password. We then try to authenticate the user using Django’s default authentication (checking username and password against what’s stored in the database). If the authentication fails, we return error message along with http status code 401. If the authentication succeeds, we issue a token for the user and pass it in the response.

We need to add this view to our urlpatterns next:

```
url(r'^login', login)
```

Now let’s try it out:

```
$ curl --request POST \
  --url http://localhost:8000/api/login \
  --header 'content-type: application/json' \
  --data '{"username": "test_user", "password": "awesomepwd"}'

{"token":"5e2effff34c85c11a8720a597b96d73a4634c9ad"}%
```

So we’re getting the tokens successfully. Now to access a secured resource, we need to pass it as part of the authorization header. But how do we make a resource available only to a logged in user? Well, permissions come into play here.

## Permissions

While authentication tells us which user is logged in (or not), it’s our responsibility to check if the current user (a valid logged in user or a guest, not logged in visitor) has access to the resource. Permissions can help us deal with that. Just like authentication, we can also set a class of permissions globally or on each resource individually. Let’s start with the `IsAuthenticated` permission first. Let’s add this to our `SubscriberViewSet`.

```
from rest_framework.permissions import IsAuthenticated


class SubscriberViewSet(ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
    permission_classes = (IsAuthenticated,)
```

If we try to access subscribers without any authentication, we will get an error message now:

```
{
  "detail": "Authentication credentials were not provided."
}
```

So let’s provide authentication using the token we got.

```
$ curl -H "Content-Type: application/json" -H "Authorization: Token 5e2effff34c85c11a8720a597b96d73a4634c9ad" http://localhost:8000/api/subscribers/
```

Now it works fine! There are many useful, already provided permission classes with Django REST Framework. You can find a list of them here [DRF API Permissions](http://www.django-rest-framework.org/api-guide/permissions/#api-reference).

## Custom Authentication and Permissions

The authentication and permission classes which come with DRF are quite enough for many cases. But what if we needed to create our own? Let’s see how we can do that.

Writing a custom authentication class is very simple. You define your custom `authenticate` method which would receive the `request` object. You will have to return an instance of the default `User` model if authentication succeeds, otherwise raise an exception. You can also return an optional value for the `auth` object to be set on `request`. If our authentication method can not be used for this request, we should return `None` so other classes are tried.

Here’s an example from DRF docs:

```
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
```

In this example, the username is being retrieved from a custom header (`X_USERNAME`) and the rest is quite easy to understand.

Next, let’s see how we can create our custom permission class. For permissions, we can have two types of permissions – global permission or per object permission. Here’s an example of global permission from DRF docs:

```
from rest_framework import permissions


class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()

        return not blacklisted
```

If the `has_permission` method returns True then the user has permission, otherwise not. Let’s see the example for per object permission:

```
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```

For dealing with per object permission, we can override the `has_object_permission` method. It can take the `request`, the `view` and the `obj`. We have to check if the current user can access the `obj` in question. Just like before, we need to return `True` or `False` to allow or deny the request.

In this blog post, we learned the basics of authentication and permissions. We now know how we can secure our API endpoints with DRF. While the token based authentication was very useful, we kind of like JWT. So in our next post, we will be using a third party package to implement JWT for Django REST Framework.
