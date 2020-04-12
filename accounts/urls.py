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
    path('account_manage', views.account_manage, name='account_manage'),
    path('pw_change/', views.pw_change, name='pw_change'),
    path('account_delete_confirmation', views.account_delete_confirmation, name='account_delete_confirmation'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('username_change/', views.change_username, name='change_username')
    
]