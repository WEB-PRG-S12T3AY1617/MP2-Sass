from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import posts.models
from . import actions, forms, models

# Create your views here.
def index(request, response=None):
    if actions.isLoggedIn(request) or 'email' in request.GET:

        if 'email' in request.GET:
            email = request.GET['email']

            try:
                user = models.User.objects.get(email=email)
            except models.User.DoesNotExist:
                user = None

        else:
            email = request.session['userMail']
            user = models.User.objects.get(email=email)

        db = posts.models.Post.objects.filter(user__email=email).order_by("-date_created")

        return render(request, 'users/index.html', {'title': 'View Profile', 'isLoggedIn': actions.isLoggedIn(request), 'query': db,
                                                    'user': user, 'styles': {'posts'}, 'scripts': {'posts'}, 'form': [forms.LogInForm],
                                                    'buttons': {
                                                        'Log In': {
                                                            'class': 'btn btn-primary',
                                                            'id': 'btnLogin',
                                                            'type': 'submit'
                                                        }
                                                    }, })
    else:
        return render(request, 'users/index.html', {'title': 'Account Log In', 'isLoggedIn': False, 'user': None,
                                                    'form': [forms.LogInForm], 'response': response,
                                                    'scripts': {'login'},
                                                    'buttons': {
                                                        'Log In': {
                                                            'class': 'btn btn-primary',
                                                            'id': 'btnLogin',
                                                            'type': 'submit'
                                                        }
                                                    }, })


def register(request, response=None):
    if actions.isLoggedIn(request) or (response and response.get('success') == True):
        return index(request)
    else:
        return render(request, 'users/register.html', {'title': 'Account Register', 'isLoggedIn': False,
                                                       'form': {forms.RegisterForm}, 'response': response,
                                                       'scripts': {'register'},
                                                       'buttons': {
                                                           'Register': {
                                                               'class': 'btn btn-primary',
                                                               'id': 'btnRegister',
                                                               'type': 'submit'
                                                           }
                                                       },
                                                       })