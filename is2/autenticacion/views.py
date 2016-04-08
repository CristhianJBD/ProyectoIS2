from django.shortcuts import render_to_response
from django.shortcuts import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf

# Create your views here.


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect('/loggedin')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('autenticacion/login_view.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponsePermanentRedirect('/loggedin')
    else:
        return HttpResponsePermanentRedirect('/invalid')

def loggedin(request):
     if request.user.is_authenticated():
         return render_to_response('autenticacion/loggedin.html', {'full_name': request.user.username})
     else:
         return HttpResponsePermanentRedirect('/login')

def invalid(request):
    return render_to_response('autenticacion/invalid.html')








