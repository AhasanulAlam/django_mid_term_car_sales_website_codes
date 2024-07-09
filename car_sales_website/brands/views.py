from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def add_brand(request):
    if request.method =='POST': # user sent POST request
        brand_form = forms.BrandForm(request.POST)  # capture the user post data
        if brand_form.is_valid(): # checking the post data validation
            brand_form.save() # if data valid save in the database
            return redirect('add_brand')  # redirect to the page 
    else:
        brand_form = forms.BrandForm()  # user will get the blank form
    return render(request, 'add_brand.html', {'form' : brand_form})