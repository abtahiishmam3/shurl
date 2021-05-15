from django.contrib import admin
from django.urls import path
from authentication.views import  signin, signup, signout
from urlhandler.views import dashboard, generate, home, stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('signout/', signout, name='signout'),
    path('generate/', generate, name='generate'),
    path('<str:query>', home, name='home'),
    path('<str:query>/stats', stats, name='stats'),
]
