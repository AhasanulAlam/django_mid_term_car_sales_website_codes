from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms
from . import models
from .models import Car, Purchase
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


# Create your views here.
# ADD CAR USING CLASS BASED CREATEVIEW:
@method_decorator(login_required, name='dispatch')
class addCarCreateView(CreateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html' # Assigning the template
    success_url = reverse_lazy('add_car')   # redirect to the page 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
# UPDATE CAR USING CLASS BASED UPDATEVIEW:
@method_decorator(login_required, name='dispatch')
class EditCarView(UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html'  # Assigning the template
    pk_url_kwarg = 'id' # getting the id
    success_url = reverse_lazy('user_profile')   # redirect to the page 

# DELETE CAR USING CLASS BASED DELETEVIEW:
@method_decorator(login_required, name='dispatch')
class DeleteCarView(DeleteView):
    model = models.Car
    template_name = 'delete.html'  # Assigning the template
    pk_url_kwarg = 'id' # getting the id
    success_url = reverse_lazy('user_profile')   # redirect to the page 

# DETAILS CAR USING CLASS BASED DETAILVIEW:
class DetailCarVied(DetailView):
    model = models.Car
    pk_url_kwarg = 'id' # getting the id
    template_name = 'car_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        carObj = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = carObj
            new_comment.save()
        return self.get( request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object # Taking the object of car model
        comments = car.comments.all()
        comment_form = forms.CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


@login_required
def buy_car(request, id):
    car = get_object_or_404(Car, id=id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        purchase, created = Purchase.objects.get_or_create(user=request.user)
        purchase.purchased_cars.add(car)
        messages.success(request, 'Car purchased successfully!')
    else:
        messages.error(request, 'Sorry, this car is out of stock.')
    return redirect('details_car', id=id)

