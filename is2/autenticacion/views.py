from django.shortcuts import render_to_response
from django.shortcuts import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf




def login_view(request):
    """
    Recibe de request los datos del usuario guardado que no cerro sesion.
    Si el usuario esta autenticado entonces ingresa al sistema(se dirige a loggedin)
    Si no lo esta muestra la interfaz de login_view para introducir los datos del usuario.


    """
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect('/loggedin')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('autenticacion/login_view.html', c)

def auth_view(request):
    """
    Recibe los parametros username y password de request.POST.
    Seguidamente se guarda en user, para luego corroborar si existe en la
    base de datos, si existe entonces se ingresa, sino se muestra un mensaje de advertencia

    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponsePermanentRedirect('/loggedin')
    else:
        return HttpResponsePermanentRedirect('/invalid')

def loggedin(request):
     """
     Si request.user estar auntenticado muestra un mensaje de bienvenida para ese usuario.
     sino se redirige a login para volver a introducir los datos


     """
     if request.user.is_authenticated():
         return render_to_response('autenticacion/loggedin.html', {'full_name': request.user.username})
     else:
         return HttpResponsePermanentRedirect('/login')

def invalid(request):
    """
    Se dirige a invalid si esque es un usuario no registrado.

    """
    return render_to_response('autenticacion/invalid.html')








