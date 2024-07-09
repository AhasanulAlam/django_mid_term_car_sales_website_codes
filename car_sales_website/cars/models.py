from django.db import models
from brands.models import Brand
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=55)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    description = models.TextField(default="")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) # One car will have multiple Brands, and multiple cars have in one Brand
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # CASCADE will delete all the posts for this user 
    image = models.ImageField(upload_to='cars/media/uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) # Capture the time of created object

    def __str__(self):
        return f"Comments by {self.name}"
    
class Purchase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purchased_cars = models.ManyToManyField(Car, blank=True)

    def __str__(self):
        return self.user.username    