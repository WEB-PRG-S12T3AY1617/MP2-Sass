"""nb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views, controllers

urlpatterns = [
    url(r'^offer/accept/', controllers.accept),
    url(r'^offer/reject/', controllers.reject),
    url(r'^offer/cancel/', controllers.cancel),
    url(r'^offer/update/', controllers.update),
    url(r'^offer/viewOffers/', controllers.viewOffers, name='viewOffers'),
    url(r'^offer/myOffers/', controllers.myOffers, name='myOffers'),
    url(r'^offer/act/', controllers.offerAct),
    url(r'^offer/offer/', controllers.offer, name='offer'),
    url(r'^get/user/', controllers.getUser),
    url(r'^get/item/', controllers.getItem),
    url(r'^sell/act/', controllers.sellAct),
    url(r'^$', views.index, name='postsIndex'),
    url(r'^sell/', views.sell, name='postsSell'),
]
