from django.http import JsonResponse, HttpResponse
from . import actions, forms, models, views

def loginAct(request):
    response = dict(success = False)
    if request.method == 'POST':
        form = forms.LogInForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            try:
                account = models.User.objects.get(email=email)

                if account.password == actions.encrypt(password, account.salt):
                    request.session['userMail'] = account.email
                    response = dict(success = True)
                else:
                    response = dict(success = False, error = 'Password is incorrect')
            except models.User.DoesNotExist:
                response = dict(success = False, error = 'Account does not exist')
        else:
            response = dict(success = False, error = form.errors)

        # return JsonResponse(request.POST, safe=False)
        if 'ajax' in request.POST:
            return JsonResponse(response)
        else:
            return JsonResponse(dict(wow=1))

def logout(request):
    if actions.isLoggedIn(request):
        request.session.flush()
    return views.index(request, None)


def registerAct(request):
    response = dict(success = False, error='Invalid action')

    if request.method == 'POST':
        salt = actions.generateSalt(8)
        password = actions.encrypt(request.POST.get('password'), salt)
        user = models.User(salt=salt, password=password)

        form = forms.RegisterForm(data=request.POST, files=request.FILES, instance=user)

        if form.is_valid():

            account = models.User.objects.filter(email=form.data.get('email'))

            if account.count() < 1:
                if form.data.get('contact_num'):
                    account = models.User.objects.filter(contact_num=form.data.get('contact_num'))

                    if account.count() < 1:
                        frm = form.save(commit=False)
                        frm.password = password
                        frm.salt = salt
                        frm.save()

                        response = dict(success=True)
                    else:
                        response = dict(success=False, error='Contact Number is already in use')
                else:
                    frm = form.save(commit=False)
                    frm.password = password
                    frm.salt = salt
                    frm.save()
                    response = dict(success = True)

            else:
                response = dict(success = False, error = 'Email is already taken')

        else:
            print(request.POST)
            response = dict(success = False, error = form.errors)

    if 'ajax' in request.POST:
        return JsonResponse(response)
    elif response['success'] == True:
        return views.index(request, None)
    else:
        return views.register(request, response)

def viewProfile(request):
    return views.index(request=request)
