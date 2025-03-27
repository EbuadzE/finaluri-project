from django.db import models
from django.contrib.auth.models import User
from newapp.models import MyCars
from decimal import Decimal



class Reserv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#ეს მოდელი არის ცალკე ელემენტი ჯავშანში, ე.ი. კონკრეტული მანქანა, რომელიც დაჯავშნა მომხმარებელმა.
class ReservItem(models.Model):
    reserv = models.ForeignKey(Reserv, on_delete=models.CASCADE)
    car = models.ForeignKey(MyCars, on_delete=models.CASCADE)
    start_date = models.DateField()  # The start date of the rental
    end_date = models.DateField()  # The end date of the rental

    # ეს არის მოდელის თვისება, რომელიც ითვლის ჯამურ ღირებულებას ამ ჯავშნის ერთეულისთვის. ის ამრავლებს დაჯავშნილი მანქანების რაოდენობას (თვითონ. რაოდენობა) მანქანის ფასზე (self.car.price).

    @property
    def rental_duration(self):
        return (self.end_date - self.start_date).days  # Calculate the number of days rented

    @property
    def amount(self):
        # ფასს ითვლის გაქირავების პერიოდის მიხედვით
        return Decimal(self.rental_duration * self.car.rental_price if self.car else Decimal('0.00'))

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    car = models.ForeignKey(MyCars, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def amount(self):
        rental_duration = (self.end_date - self.start_date).days
        return Decimal(rental_duration * self.car.rental_price if self.car else Decimal('0.00'))








































