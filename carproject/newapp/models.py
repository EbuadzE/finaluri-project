from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class MyCars(models.Model):
    model = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    firm = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(default="No description")
    category = models.ManyToManyField(Category, related_name = 'car_category')
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='cars', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model






