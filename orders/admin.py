from django.contrib import admin
from .models import  Topping, Category, Size, Order, Pizza, Pasta, Salad, Subs, DinnerPlatters, Pedido, Order
from django.core.mail import send_mail

# Register your models here.


class PizzaAdmin(admin.ModelAdmin): 
    filter_horizontal = ('topping',)
    list_display = ('category', 'name', 'size', 'price', 'id')
    list_editable = ('price',)
    list_filter = ('category',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'status', 'user')
    filter_horizontal = ('pedidos',)

class PastaAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'price')
    list_editable = ('price',)
class SaladAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'price')
    list_editable = ('price',)
class DinnerPlattersAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'size', 'price')
    list_editable = ('price',)
class SubsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'size', 'price', 'id')
    list_editable = ('price',)
class PedidoAdmin(admin.ModelAdmin):
    filter_horizontal = ('topping',)
    list_display = ( 'user','name', 'price', 'size', 'category', 'numberOrder')
    list_editable = ('price',)
    list_filter = ('user',)


admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Subs, SubsAdmin)
admin.site.register(DinnerPlatters, DinnerPlattersAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(Pedido, PedidoAdmin)


