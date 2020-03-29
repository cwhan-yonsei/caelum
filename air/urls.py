from django.urls import path, include
from . import views

app_name = 'air'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.article, name='article'),
    path('edit_article/<int:pk>', views.edit_article, name='edit_article'),
    path('del_article/<int:pk>', views.del_article, name='del_article'),
    path('question/', views.question, name='question'),
    path('answer/<int:pk>/', views.answer, name='answer'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('del_comment/<int:pk>/', views.del_comment, name='del_comment'),
]