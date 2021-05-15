from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from urlhandler.views import home



def signin(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            try:
                user = User.objects.get(email=request.POST['email'])
                auth.login(request, user)
                if request.POST['next'] != '':
                    return redirect(request.POST.get('next'))
                else:
                    return redirect(home)
                return redirect(home)
            # render(request, 'login.html', {})
            except User.DoesNotExist:
                return render(request, 'login.html', {'error': 'Please create an account first'})
    return render(request, 'login.html', {})


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email = request.POST['email'])
                    return render(request, 'signup.html', {'error': "User already exists"})
                except User.DoesNotExist:
                    User.objects.create_user(
                        username=request.POST['username'],
                        email=request.POST['email'],
                        password=request.POST['password']
                    )
                    messages.success(request, 'Sign up successful, login here')
                    return redirect(signin)

            else:
                return render(request, 'signup.html', {'error': "Empty fields exist"})
        else:
            return render(request, 'signup.html', {'error': "Passwords don't match"})
    return render(request, 'signup.html', {})


def signout(request):
    auth.logout(request)
    # request.user.is_authenticated = False
    return redirect(signin)

