from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.utils import ErrorList

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None, portal_id=None, name=None, dept_major=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute, renderer=renderer)
        self.portal_id = portal_id
        self.name = name
        self.dept_major = dept_major

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.portal_id = self.portal_id
        user.name = self.name
        user.dept_major = self.dept_major
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('password', 'username')

    def clean_password(self):
        return self.initial['password']

class AdminUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'portal_id', 'dept_major', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

class YonseiVerificationForm(forms.Form):
    privacy_consent = forms.BooleanField(label='privacy_consent')
    portal_id = forms.CharField(label='portal_id')
    portal_pw = forms.CharField(label='portal_pw', widget=forms.PasswordInput)

class PasswordResetForm(forms.ModelForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(label='New username', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
    