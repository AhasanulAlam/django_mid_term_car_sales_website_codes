from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addCarCreateView.as_view(), name='add_car'),
    path('edit/<int:id>/', views.EditCarView.as_view(), name='edit_car'),
    path('delete/<int:id>/', views.DeleteCarView.as_view(), name='delete_car'),
    path('details/<int:id>/', views.DetailCarVied.as_view(), name='details_car'),
    path('buy/<int:id>/', views.buy_car, name='buy_car'),
]
