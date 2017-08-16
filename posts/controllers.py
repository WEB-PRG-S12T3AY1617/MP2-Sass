import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from posts.forms import OfferForm
from posts.models import Post, Offer
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


def myOffers(request):
    if 'userMail' in request.session:
        try:
            user = User.objects.get(email=request.session['userMail'])
        except:
            return HttpResponseRedirect('/')

        offers = Offer.objects.filter(offerFrom=user)

        return render(request, 'posts/myOffers.html', {'title': 'View Offers', 'offers': offers, 'isLoggedIn': True,
                                                       'styles': {'posts'}, 'scripts': {'posts'}})
    else:
        return HttpResponseRedirect('/')

def cancel(request):
    if 'offer' in request.GET:
        try:
            offer = Offer.objects.get(id=request.GET['offer'])
            offer.delete()

            return HttpResponseRedirect('/posts/offer/myOffers/')
        except Offer.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def viewOffers(request):
    if 'userMail' in request.session:
        try:
            user = User.objects.get(email=request.session['userMail'])
        except:
            return HttpResponseRedirect('/')

        offers = Offer.objects.filter(post__user=user)

        return render(request, 'posts/viewOffers.html', {'title': 'View Offers', 'offers': offers, 'isLoggedIn': True,
                                                         'styles': {'posts'}, 'scripts  ': {'posts'}})
    else:
        return HttpResponseRedirect('/')

def offer(request, response=None):
    if 'user' in request.GET and 'userMail' in request.session:
        try:
            sender = User.objects.get(email=request.session['userMail'])
            receiver  = User.objects.get(pk=request.GET['user'])

            offerForm = OfferForm(sender=sender, receiver=receiver)

            return render(request, 'posts/offer.html', {'response': response, 'title': 'Offer/Buy from <i>' + receiver.name + "</i>", 'form': {offerForm}, 'isLoggedIn': 'userMail' in request.session, 'buttons': {
                                                       'Make/Update an Offer': {
                                                           'class': 'btn btn-primary',
                                                           'type': 'submit',
                                                           'id': 'btnOffer',
                                                       }
                                                   }})
        except User.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def offerAct(request):
    if request.method == 'POST':
        try:
            try:
                post = Post.objects.get(pk=request.POST['post'])
            except Post.DoesNotExist:
                return offer(request, dict(success=False, error='Post offering does not exist'))

            sender = User.objects.get(email=request.session['userMail'])
            receiver = User.objects.get(pk=post.user.id)

            offerForm = OfferForm(data=request.POST, sender=sender, receiver=receiver)

            if offerForm.is_valid():
                off = offerForm.save(commit=False)
                off.offerFrom = sender
                off.save()

                return views.index(request)
            else:
                return offer(request, dict(success=False, error=offerForm.errors))
        except User.DoesNotExist:
            return offer(request, dict(success=False, error=' Uh Oh! Something wrong happened'))
    else:
        return offer(request, dict(success=False, error='Oops! We encountered a problem'))


def update(request):
    if 'post' in request.POST and 'userMail' in request.session:
        try:
            user = User.objects.get(email=request.session['userMail'])

            try:
                offer = Offer.objects.get(offerFrom=user, post_id=request.POST['post'])
                offerForm = OfferForm(data=request.POST, instance=offer, sender=user, receiver=offer.post.user)

                if offerForm.is_valid():
                    offerForm.save()


                return HttpResponseRedirect('/posts/offer/myOffers/')
            except Offer.DoesNotExist:
                return HttpResponseRedirect('/')

        except User.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def accept(request):
    if 'userMail' in request.session and 'offer' in request.GET:
        try:
            offer = Offer.objects.get(pk=request.GET['offer'])

            offer.accepted = True
            offer.save()

            return HttpResponseRedirect('/posts/offer/viewOffers/')
        except:
            return HttpResponseRedirect('/posts/offer/viewOffers/')
    else:
        return HttpResponseRedirect('/')


def reject(request):
    if 'userMail' in request.session and 'offer' in request.GET:
        try:
            offer = Offer.objects.get(pk=request.GET['offer'])

            offer.rejected = True
            offer.save()

            return HttpResponseRedirect('/posts/offer/viewOffers/')
        except:
            return HttpResponseRedirect('/posts/offer/viewOffers/')
    else:
        return HttpResponseRedirect('/')