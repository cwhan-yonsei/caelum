from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from .forms import UserCreationForm, UserChangeForm

# Create your views here.
def landing(request):
     if request.method == 'POST':
          form = AuthenticationForm(request, request.POST)
          if form.is_valid():
               login(request, form.get_user())
               return redirect('air:index')
# What if not vaild?

     elif request.method == 'GET':
          form = AuthenticationForm()
          context = {
               'form': form,
          }
          return render(request, 'accounts/landing.html', context)

def sign_up(request):
     if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
               form.save()
          return redirect('air:index')
# What if the form is not valid?

     elif request.method == 'GET':
          form = UserCreationForm()
          context = {
               'form': form,
          }
          return render(request, 'accounts/sign-up.html', context)