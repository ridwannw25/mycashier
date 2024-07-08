from .views import Auth
from django.urls import path

urlpatterns = [
    path('login', Auth.login),
    path('logout', Auth.logout),
    # path('accounts/', include('django.contrib.auth.urls')),
]