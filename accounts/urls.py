from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('verification/', views.verification, name='verification'),
    path('signup/', views.sign_up, name='sign_up'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('findaccount/', views.find_account, name='find_account'),
    path('pwreset/<str:uidb64>/<str:token>', views.pw_reset, name='pw_reset'),
    path('signout', views.sign_out, name='sign_out'),
]