"""rest_framework_queryset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from api.views import ListView
from web.views import ListDataView

router = routers.SimpleRouter()
router.register(r'api', ListView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', ListView.as_view()),
    url(r'^list/$', ListDataView.as_view()),
    url(r'^list/page/(?P<page>\d+)/$', ListDataView.as_view()),
] + router.urls
