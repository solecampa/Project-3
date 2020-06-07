from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topping(models.Model):
    item = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.item}"

class Category(models.Model):
    tipo = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.tipo} "

class Size(models.Model):
    size = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.size}  " 


class Pizza(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categoria")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="tamaño_Pizza")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    topping = models.ManyToManyField(Topping, blank=True, related_name="Pizza_topping")
    def __str__(self):
        return f"{self.category} {self.name} {self.size} {self.id}"

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f" {self.name} "
        
class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f" {self.name} " 

        
class Subs(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="tamaño_Subs")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    topping = models.ManyToManyField(Topping, blank=True, related_name="Subs_topping")
    def __str__(self):
        return f" {self.name} {self.size} {self.id}"

class DinnerPlatters(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="tamaño_Dinner")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f" {self.name} {self.size}"



class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Usuario") 
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=64, blank=True, null=True)
    size = models.CharField(max_length=64, blank=True, null=True)
    topping = models.ManyToManyField(Topping, blank=True, related_name="Pedido_toppings")
    numberOrder= models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.user} -{self.category} {self.name} - {self.size} - {self.price} - nro ={self.numberOrder}  "

class Order(models.Model):

    STATUS = [
    ('I', 'Iniciated'),
    ('F', 'Finished'),
    ('D', 'Delivered')

    ]

    pedidos = models.ManyToManyField(Pedido, blank=True, related_name="orden")
    status = models.CharField(max_length=64, choices=STATUS, default='Iniciated')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    def __str__(self):
        return f"{self.id}-{self.status}"



