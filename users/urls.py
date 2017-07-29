from django.conf.urls import url
from . import views, controllers

urlpatterns = [
    url(r'^view/$', controllers.viewProfile),
    url(r'^login/act/ajax/', controllers.loginAct, name='loginAct'),
    url(r'^login/act/', controllers.loginAct, name='loginAct'),

    url(r'^logout/act/', controllers.logout, name='logoutAct'),

    url(r'^register/act/ajax/', controllers.registerAct, name='registerAct'),
    url(r'^register/act/', controllers.registerAct, name='registerAct'),

    url(r'^login/', views.index, name='login'),
    url(r'^register/', views.register, name='register'),

    url(r'^$', views.index, name='userIndex')
]
