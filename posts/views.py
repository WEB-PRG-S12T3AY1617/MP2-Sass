from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import forms, models,controllers
from users import actions, views

# Create your views here.
def index(request, response=None):
    db = models.Post.objects.all()

    limit = 10
    tags = None
    use = 0
    uid = None

    if 'limit' in request.GET:
        limit = request.GET['limit']

    if 'user' in request.GET:
        db = controllers.narrowPost(db=db, user=request.GET['user'])
        uid = request.GET['user']

    if 'type' in request.GET:
        use = request.GET['type']
        if use > '-1':
            db = controllers.narrowPost(db=db, type=request.GET['type'])

    if 'tags' in request.GET and request.GET['tags']:
        tags = request.GET['tags']
        db = controllers.narrowPost(db=db, tag=request.GET['tags'])

    db = db.order_by("-date_created")

    paginator = Paginator(db, limit)
    page = 1

    if 'page' in request.GET:
        page = request.GET['page']

    try:
        db = paginator.page(page)
    except PageNotAnInteger:
        db = paginator.page(1)
    except EmptyPage:
        db = paginator.page(paginator.num_pages)

    return render(request, 'posts/index.html', {'title': 'View Posts', 'response': response, 'isLoggedIn': actions.isLoggedIn(request),
                                                'query': db, 'styles': {'posts'}, 'scripts': {'posts'},'pageNum': page, 'tags': tags,
                                                'type': use, 'limit': limit, 'hasModal': True, 'user': uid})


def sell(request, response=None):
    if not actions.isLoggedIn(request):
        return views.index(request, None)
    else:
        return render(request, 'posts/sell.html', {'title': 'Sell an Item', 'form': [forms.ItemForm, forms.PostForm],
                                                   'isLoggedIn': True, 'response': response, 'scripts': {'sell'},
                                                   'buttons': {
                                                       'Post Item': {
                                                           'class': 'btn btn-primary',
                                                           'type': 'submit',
                                                           'id': 'btnPostItem',
                                                       }
                                                   }})