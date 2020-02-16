from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied

from .forms import UserCreationForm, UserChangeForm, YonseiVerificationForm

import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome


def identify(portal_id, portal_pw):
     options = webdriver.ChromeOptions()
     driver = webdriver.Chrome('/home/cwahn/yonsei/caelum/downloads/chromedriver', options=options)
     portal_url = 'https://portal.yonsei.ac.kr/main/index.jsp'
     driver.get(portal_url)

     driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
     try:
          driver.find_element_by_xpath('//*[@id="loginId"]').send_keys(portal_id)
          driver.find_element_by_xpath('//*[@id="loginPasswd"]').send_keys(portal_pw)
          driver.find_element_by_xpath('//*[@onclick="fSubmitSSOLoginForm()"]').click()

          driver.find_element_by_xpath('//*[@id="jooyohaksalink1"]').click()
     
     except:
          driver.quit()
          return False, '', ''

     driver.find_element_by_xpath('//*[@id="btn_lang"]').click()

     driver.find_element_by_xpath('//*[@id="btn_open_icon"]').click()

     name = driver.find_element_by_xpath('//*[@id="wq_uuid_63"]').text
     dept_major = driver.find_element_by_xpath('//*[@id="wq_uuid_77"]').text

     driver.quit()

     return True, name, dept_major


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
          if form.is_valid() and form.cleaned_data.get('privacy_consent'):
               portal_id = form.cleaned_data.get('portal_id')
               portal_pw = form.cleaned_data.get('portal_pw')
               result =  identify(portal_id, portal_pw)
               if result[0] == True and portal_id[4] == '1':
                    request.session['pid'] = portal_id
                    request.session['name'] = result[1]
                    request.session['dept_major'] = result[2]
                    request.session['verification'] = True

                    return redirect('accounts:sign_up')
                    
               else:
                    return redirect('accounts:landing')
          else:
               return redirect('account:landing')

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
          form = UserCreationForm()
          context = {
               'form': form,
          }
          return render(request, 'accounts/sign-up.html', context)