from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied

from .forms import UserCreationForm, UserChangeForm, YonseiVerificationForm

from .yonsei_auth import verify

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


def verification(request):
    if request.method == 'POST':
        form = YonseiVerificationForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('privacy_consent') == True:
            portal_id = form.cleaned_data.get('portal_id')
            portal_pw = form.cleaned_data.get('portal_pw')
            result, name, dept_major = verify(portal_id, portal_pw)

            if result == True:
                request.session['pid'] = portal_id
                request.session['name'] = name
                request.session['dept_major'] = dept_major
                request.session['verification'] = True

                return redirect('accounts:sign_up')
            else:
                # not yonsei student
                return redirect('accounts:landing')
        else:
            return redirect('accounts:landing')

    elif request.method == 'GET':
        form = YonseiVerificationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/verification.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('air:index')
# What if the form is not valid?

    elif request.method == 'GET':
        if request.session['verification'] == True:

            context = {
                'form': UserCreationForm(),
                'portal_id': request.session['pid'],
                'name': request.session['name'],
                'dept_major': request.session['dept_major'],
            }
            return render(request, 'accounts/sign-up.html', context)
        else:
            return redirect('accounts:landing')

