import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from . import views, models, forms
from users.models import User

def sellAct(request):
    response = dict(success = False, error = {})

    if(request.method == 'POST'):
        itemForm = forms.ItemForm(request.POST, request.FILES)

        if itemForm.is_valid():
            try:
                user = User.objects.get(email=request.session['userMail'])

                item = itemForm.save()
                postForm = forms.PostForm(request.POST)

                if postForm.is_valid():
                    post = postForm.save(commit=False)
                    post.item = item
                    post.user = user
                    post.save()

                    response = dict(success = True)
                else:
                    response = dict(success = False, error = postForm.errors)

            except User.DoesNotExist:
                response = dict(success = False, error = 'User is not logged in')
        else:
            response = dict(success = False, error = itemForm.errors)

        if 'ajax' in request.POST:
            return JsonResponse(response)
        else:
            return views.sell(request, response)

def narrowPost(db=None, type=None, tag=None, user=None):
    if db == None:
        db = models.Post.objects.all()

    if user:
        try:
            db = db.filter(user=User.objects.get(id=user))
        except User.DoesNotExist:
            db = db

    if type != None:
        db = db.filter(item__use=type)

    if tag:
        tags = tag.split()
        limit = Q()

        for t in tags:
            limit = limit | Q(tags__contains=t)

        db = db.filter(limit)

    return db


def getItem(request):
    try:
        db = models.Item.objects.get(id = request.GET.get("id"))
        return JsonResponse(dict(success = True, item=serializers.serialize('json', [db])))
    except models.Item.DoesNotExist:
        return JsonResponse(dict(success = False))


def getUser(request):
    try:
        db = models.User.objects.get(id = request.GET.get("id"))
        return JsonResponse(dict(success = True, user=serializers.serialize('json', [db])))
    except models.Item.DoesNotExist:
        return JsonResponse(dict(success = False))
