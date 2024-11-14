from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import Logout_View

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
]
