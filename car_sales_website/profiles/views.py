from django.shortcuts import render, redirect
from . import forms
from cars.models import Car
from cars.models import Purchase
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def register(request):
    if request.method =='POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'User Account Created Successfully!')
            return redirect('register')
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})

# LOGIN USING CLASS BASED LOGINVIEW:
class UserLoginView(LoginView):
    template_name = 'register.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'User Logged In Successfully!')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, 'Incorrect Logged In Information!')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


# LOGOUT USING CLASS BASED LOGOUTVIEW:
class UserLogoutView(LogoutView):
    def get_success_url(self):
        messages.warning(self.request, 'User Logged Out Successfully!')
        return reverse_lazy('homepage')
 

# @login_required
# def user_profile(request):
#     data = Car.objects.filter(user = request.user)
#     return render(request, './profile.html', {'data' : data,  'type' : 'Profile'})

@login_required
def user_profile(request):
    purchase, created = Purchase.objects.get_or_create(user=request.user)
    purchased_cars = purchase.purchased_cars.all()
    data = Car.objects.filter(user=request.user)
    return render(request, './profile.html', {'data': data, 'purchased_cars': purchased_cars, 'type': 'Profile'})




@login_required
def edit_profile(request):
    if request.method =='POST':
        profile_form = forms.changeUserDataForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated Successfully!')
            return redirect('user_profile')
    else:
        profile_form = forms.changeUserDataForm(instance = request.user)
    return render(request, './update_profile.html', {'form' : profile_form, 'type' : 'Edit Profile'})

@login_required
def pass_change(request):
    if request.method =='POST':
        pass_change_form = PasswordChangeForm(request.user, data = request.POST)
        if pass_change_form.is_valid():
            pass_change_form.save()
            messages.success(request, 'Password Updated Successfully!')
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('user_profile')
    else:
        pass_change_form = PasswordChangeForm(user = request.user)
    return render(request, './pass_change.html', {'form' : pass_change_form, 'type' : 'Password Change'})

