from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import sys
from django.db import models
from django.db.models import Sum
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from .models import Topping, Category, Size,  Pizza, Pasta, Salad, Subs, DinnerPlatters, User, Pedido, Order

# Create your views here.

context1 = {
    "Regular": Pizza.objects.all().filter(category=1, size=1),
    "RegularSmall": Pizza.objects.all().filter(category=1, size=1),
    "RegularLarge": Pizza.objects.all().filter(category=1, size=2),
    "Sicilian": Pizza.objects.all().filter(category=2, size=1),
    "SicilianSmall": Pizza.objects.all().filter(category=2, size=1),
    "SicilianLarge": Pizza.objects.all().filter(category=2, size=2),
    "Toppings": Topping.objects.all(),
    "Pasta": Pasta.objects.all(),
    "Salad": Salad.objects.all(),
    "Subs": Subs.objects.all().filter(size=2),
    "SubsSmall": Subs.objects.all().filter(size=1),
    "SubsLarge": Subs.objects.all().filter(size=2),
    "DinnerPlatters": DinnerPlatters.objects.all(),
    "SDinnerPlatters": DinnerPlatters.objects.all().filter(size=1),
    "LDinnerPlatters": DinnerPlatters.objects.all().filter(size=2),
    
    
    
}



def index(request):
    return render(request, "orders/index.html", context1)

def orders(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "orders/login.html")
        user = request.user
        contador = Pedido.objects.all().filter(user=user.id).count()
        context1["contador"] = contador
        return render(request, "orders/orders2.html", context1)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "orders/login.html")
        user = request.user
        contador = Pedido.objects.all().filter(user=user.id).count()
        context1["contador"] = contador
        j = request.POST["selection"]
        q = request.POST["class"]
        t = request.POST.get("topping")
        t2A = request.POST.get("2toppingA")
        t2B = request.POST.get("2toppingB")
        t3 = request.POST.get("3topping")
        
       
        def str_to_class(str):
            return getattr(sys.modules[__name__], str)
        b = str_to_class(q).objects.get(pk=j)
        name= b.name
        price = b.price
        order = Order.objects.all().filter(user=user).first()
        

        if q == "Pizza":
            size = b.size
            category = b.category
            pedido = Pedido(user=user, name=name, size=size, category=category, price=price)
            pedido.save()
            if b.name == "1 Topping":
                pedido.topping.add(t)
            if b.name == "2 Toppings":
                pedido.topping.add(t2A)
                pedido.topping.add(t2B)
            if b.name == "3 Toppings":
                pedido.topping.add(t2A)
                pedido.topping.add(t2B)
                pedido.topping.add(t3)                
        if q == "DinnerPlatters":
            size = b.size
            pedido = Pedido(user=user, name=name, size=size,  price=price)
            pedido.save()
        if q == "Subs":
            size = b.size
            pedido = Pedido(user=user, name=name, size=size,  price=price)
            pedido.save()
        if q == "Pasta":
            pedido = Pedido(user=user, name=name, price=price)
            pedido.save()
        if q == "Salad":
            pedido = Pedido(user=user, name=name, price=price)
            pedido.save()
        

        contador = Pedido.objects.all().filter(user=user.id).count()
        context1["contador"] = contador


        
        
        print(name)
        print(price)
        print(user.id)
        print(pedido.size)
        
       
        return render(request, "orders/orders2.html", context1, )

def yourOrder(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    user = request.user
    pedido = Pedido.objects.all().filter(user=user.id)
    suma = Pedido.objects.all().filter(user=user.id).aggregate(Sum('price'))
    contador = Pedido.objects.all().filter(user=user.id).count()
    if suma['price__sum'] == None:
        total = "0"  
    else:
        total = float(suma['price__sum'])
    context = {
        "Pedido": pedido,
        "user" : user,
        "total": total,
        "order": "" ,
        "contador": contador
    }
    if request.method == "GET":
        order = Order.objects.all().filter(user=user).first()
        if order != None:
            print(order)
            if order.status == "Iniciated":
                context["Pedido"]= "I"
                context["order"] = order
                
                print("iniciado")
            if order.status == "F":
                context["Pedido"] = "F"
                context["order"] = order
                print("finalizada")
            if order.status == "D":
                order.delete()
                context["Pedido"] = "D"
                context["order"] = "-"
                total = "0"
                for p in pedido:
                    p.delete()

        return render(request, "orders/yourOrder.html", context)
    if request.method == "POST":
        s = request.POST.get("send")
        order = Order(user=user, status="Iniciated")
        order.save()
        for p in pedido:
            order.pedidos.add(p)
        context["Pedido"]= "I"
        context["order"] = order
        send_mail('Pinoccios Pizza Order',
            'Your order is on its way',
            'sole.prueba.app@gmail.com',
            [user.email],
        )  
        return render(request, "orders/yourOrder.html", context)

    
    

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("orders"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})



def singup(request):
    if request.method == "GET":
        return render(request, "orders/singup.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        user = User.objects.create_user(first, email, password)
        user.last_name = last
        user.save()
        return HttpResponseRedirect(reverse("orders"))


