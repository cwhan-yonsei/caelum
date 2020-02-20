from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .forms import UserCreationForm, UserChangeForm, YonseiVerificationForm
from .models import User

from .yonsei_auth import verify

# Create your views here.


def landing(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_email_verified:
                login(request, user)
                return redirect('air:index')
            else: # valid but pendig email verification 
                form = AuthenticationForm()
                context = {
                            'form': form,
                            'account_error': 'Email verification is required. Please cheack your email for verification link.',
                        }
                return render(request, 'accounts/landing.html', context)
        else:
            form = AuthenticationForm()
            context = {
                        'form': form,
                        'account_error': 'Invalid account.',
                    }
            return render(request, 'accounts/landing.html', context)


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

                if not User.objects.filter(portal_id=portal_id).exists():
                    request.session['pid'] = portal_id
                    request.session['name'] = name
                    request.session['dept_major'] = dept_major
                    request.session['verification'] = True

                    return redirect('accounts:sign_up')
                else:
                    # already a member
                    return redirect('accounts:landing')
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
        form = UserCreationForm(
            request.POST,
            portal_id=request.session['pid'],
            name=request.session['name'],
            dept_major=request.session['dept_major']
        )
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request, 'Activation link is invalid!')
