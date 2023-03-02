"""pollsgh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views
from poll import views as poll_views
from people import views as people_views
from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-token-auth/', auth_views.obtain_auth_token),

    path("app/", include("accounts.urls")),
    path('app/', include('django.contrib.auth.urls')),
    # app/ login/ [name='login']
    # app/ logout/ [name='logout']
    # app/ password_change/ [name='password_change']
    # app/ password_change/done/ [name='password_change_done']
    # app/ password_reset/ [name='password_reset']
    # app/ password_reset/done/ [name='password_reset_done']
    # app/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # app/ reset/done/ [name='password_reset_complete']


    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path("geo/", include("geo.urls")),
    path("api/geo/", include("geo.api.urls")),

    path("people/", include("people.urls")),
    path("api/people/", include("people.api.urls")),

    path("poll/", include("poll.urls")),
    path("api/poll/", include("poll.api.urls")),
]
