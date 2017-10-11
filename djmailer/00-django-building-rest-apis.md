
# Django: Building REST APIs

_Written by masnunon May 13, 2017_

Recently, I have written a few pieces on REST API development. We have discussed the Fundamentals of REST APIs, Built a Simple REST API, Secured it with HTTP Basic Authentication and JSON Web Tokens. However, the example codes were all based on Flask. I chose Flask for those examples because the framework was minimal in it’s core, light weight yet popular and with a matured eco system – very well suited for demonstrating simple REST APIs. But if we consider popularity, probably no other framework is as popular as Django in the Python land. In my day to day work, I use the framework quite extensively. Over the years, I have grown to become a passionate fan of Django. Naturally a tutorial series on building REST APIs with Django was just a matter of time.

## Tutorial Index

This is the first part of the [series](http://polyglot.ninja/django-building-rest-apis/). I shall update the index here as I keep adding new contents.

* Getting Started (This post)
* Getting Started with Django REST Framework
* Serializers
* ModelSerializer and Generic Views
* ViewSet, ModelViewSet and Router
* Authentication and Permissions
* Using JWT

**Code**: https://github.com/masnun/djmailer

## Prerequisites

The tutorial series will be heavily focused on building REST APIs. So there will be less scope of discussing the fundamentals of Django as we go. I would expect the reader to have decent familiarity of Django before hand. If you are new to Django, please spend some time with the [Official Tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/). It is very well written.

The tutorial series will use Python `3.6.0` (but any versions above Python 3.0 should work fine). As for Django, I have just installed the latest release as of today –  `1.11.` . We would also be using Django REST Framework, I have `3.6.3` right now. The example code repository will have an up-to-date `requirements.txt` file – so don’t worry much about dependencies or their versions right now. Just make sure you use Python 3 and not Python 2.

## Setting Up Django

Before we can start working on our awesome REST API, we first need to setup and configure our Django project. We need to install Django, install dependencies, start a project and an app, configure the database connection and write our first view. So what are we waiting for? Let’s get started!

### Install Django and Dependencies

For now, we need the latest Django and a database driver. We will be using MySQL since it’s very popular and most people are familiar with it. In our production systems though, we mostly run PostgreSQL. We will discuss that choice in some later posts. Let’s install Django and the MySQL client using `pip`.

```
pip install django
pip install mysqlclient
```

Done? Cool. If Django installed successfully, you should be able to run the `django-admin.py` command. See if you can run it. If the command runs successfully, your installation worked. Time to move on to the next phase.

### Create the Django Project

We want to build REST APIs for a mailing list. Let’s call it `djmailer`. We use the `startproject` admin command to start our project.

```
django-admin startproject djmailer
```

We would now have a directory named `djmailer` created in the current directory. Within that, there’s the default `djmailer` app directory which contains the settings and root urlconf and the uwsgi app.

### Create a New App

For the API related stuff, we would now create a new app named `api`. Let’s do that. First cd into the project so you  can access the `manage.py` file. Now run this command:

```
python manage.py startapp api
```

Cool, now we have the `api` app created for us. Open up `djmailer/settings.py` and add `api` to the `INSTALLED_APPS` list.

### Configure Database

In the default `djmailer` app, there’s a file named `settings.py`. Open it up in your favorite text editor. We need to add our database credentials here. We will notice that a sample database configuration is already generated for us. Something like:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

The above example uses SQLite. But we want to use MySQL. So first create a database named `djmailer` on your MySQL server and create the database user and password. Then replace the above code with these lines:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djmailer',
        'USER': 'djmailer',
        'PASSWORD': 'suP3rS3CR3t!X$%^',
    }
}
```

Once you have configured the database, please run the migrate management command.

```
python manage.py migrate
```

This should create the tables Django needs for itself.

## Hello World!

Time to create our first view. Open `api/views.py` file and create the view:

```
from django.http.response import JsonResponse


def hello_world(request):
    return JsonResponse({"message": "hello world!"})
```

Instead of the usual `HttpResponse`, we used `JsonResponse` because we want to render our response as JSON. Using this class ensures that the reponse is JSON and the appropriate content type is set.

We can add this view directly to the root urlconf in `djmailer/urls.py` but we would like to better organize our urls. So we are going to create a new file named `urls.py` in the `api` directory and put the following content:

```
from django.conf.urls import url

from .views import hello_world

urlpatterns = [
    url(r'^hello', hello_world, name="hello_world")
]
```

If we add urls from all apps to the root urlconf, it will soon become a mess. Also the apps will not be reusable. But if we keep our app specific routes inside the app, we can just import them from the root urlconf. This keeps things clean and the app can be easily plugged into a different project if needed.

Let’s edit `djmailer/urls.py` (the root urlconf) and import our api urls.

```
from django.conf.urls import url, include
from django.contrib import admin

from api import urls as api_urls

urlpatterns = [
    url(r'^api/', include(api_urls, namespace="api")),
    url(r'^admin/', admin.site.urls),
]
```

Focus on line 4 and 7. We are importing our api urls and putting them under the `/api/` path. Run the django dev server:

```
python manage.py runserver
```

If we visit `http://localhost:8000/api/hello`, we would see the response:

```
{"message": "hello world!"}
```

Cool? We just built our first RESTful view with Django.

## Introducing Django REST Framework (DRF)

Building REST APIs with plain old Django is very possible but we have to do a lot. We need to read incoming requests, parse them as JSON or XML (through content negotiation), in case of CRUD operations, we also have to work with models and finally we have to send back the response in appropriate format. It’s all possible in Django – but like I said, I have to do so many things on our own. Our initial hello world view was very basic, very simple. As the project grows and we have more and more complexities, things will start to get out of hands.

In our Flask examples, using a third party extension helped us get started faster and saved us much time and efforts. Django REST Framework is one such framework for Django. It provides so much functionality out of the box – I am a big fan of the framework. So while we can do everything without this framework, using it would make us productive and keep things sane.

So from now on, we would be using DRF to continue building our APIs. In the next blog post, we would be getting started with Django REST Framework.

## What’s Next?

On our next post – Django REST Framework: Getting Started, we introduce you to the wonderful world of DRF and demonstrate how we can use `APIView` to build our endpoints.

In the mean time, please subscribe to our mailing list. We will keep you posted when we publish new content. 🙂
