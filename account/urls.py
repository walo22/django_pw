from django.contrib.auth.views import LoginView
from django.urls import path ,include
from account.forms import UserLoginForm

urlpatterns = [
   path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login'),
   path('', include('django.contrib.auth.urls'))
]