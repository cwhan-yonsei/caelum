from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('verification/', views.verification, name='verification'),
    path('signup/', views.sign_up, name='sign_up'),
]