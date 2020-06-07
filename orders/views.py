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
    "Toppings": Topping.objects.exclude(id=21).all(),
    "SubToppings": Topping.objects.all(),
    "Pasta": Pasta.objects.all(),
    "Salad": Salad.objects.all(),
    "Subs": Subs.objects.all().filter(size=2),
    "SubsSmall": Subs.objects.all().filter(size=1),
    "SubsLarge": Subs.objects.all().filter(size=2),
    "DinnerPlatters": DinnerPlatters.objects.all(),
    "SDinnerPlatters": DinnerPlatters.objects.all().filter(size=1),
    "LDinnerPlatters": DinnerPlatters.objects.all().filter(size=2),
    "message": ""
    
    
    
    
}



def index(request):
    return render(request, "orders/index.html", context1)

def orders(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "orders/login.html", {"contador": "0"})
        else:
            user = request.user
            order = Order.objects.all().filter(user=user).first()
            if order != None:
                return HttpResponseRedirect(reverse("yourOrder"))
            else:
                contador = Pedido.objects.all().filter(user=user.id).count()
                context1["contador"] = contador
                if "message" in context1:
                    del context1["message"]
                return render(request, "orders/orders2.html", context1)
                    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "orders/login.html", {"contador": "0"})
        user = request.user
        contador = Pedido.objects.all().filter(user=user.id).count()
        context1["contador"] = contador
        j = request.POST["selection"]
        q = request.POST["class"]
        t = request.POST.get("topping")
        t2A = request.POST.get("2toppingA")
        t2B = request.POST.get("2toppingB")
        t3 = request.POST.get("3topping")
        st = request.POST.get("subtopping")
        
       
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
            context1["message"] =  f"{b.name} added to your order"
            if b.name == "1 Topping":
                pedido.topping.add(t)
                top = Topping.objects.all().filter(id=t).first().item
                context1["message"] =  f"{b.name} with {top} added to your order"
            if b.name == "2 Toppings":
                pedido.topping.add(t2A)
                pedido.topping.add(t2B)
                top1 = Topping.objects.all().filter(id=t2A).first().item
                top2 = Topping.objects.all().filter(id=t2B).first().item
                context1["message"] =  f"{b.name} with {top1} and {top2} added to your order"
            if b.name == "3 Toppings":
                pedido.topping.add(t2A)
                pedido.topping.add(t2B)
                pedido.topping.add(t3)
                top1 = Topping.objects.all().filter(id=t2A).first().item
                top2 = Topping.objects.all().filter(id=t2B).first().item
                top3 = Topping.objects.all().filter(id=t3).first().item 
                context1["message"] =  f"{b.name} with {top1}, {top2} and {top3} added to your order"               
        if q == "DinnerPlatters":
            size = b.size
            pedido = Pedido(user=user, name=name, size=size,  price=price)
            pedido.save()
            context1["message"] =  f"{b.name} added to your order"
        if q == "Subs":
            size = b.size
            pedido = Pedido(user=user, name=name, size=size,  price=price)
            pedido.save()
            context1["message"] =  f"{b.name} added to your order"
            if st != "":
                pedido.topping.add(st)
                top = Topping.objects.all().filter(id=st).first().item
                pedido = Pedido(user=user, name=f" Adding {top} ", price=0.5)
                pedido.save()
                context1["message"] =  f"{b.name} + {top} added to your order"
          

        if q == "Pasta":
            pedido = Pedido(user=user, name=name, price=price)
            pedido.save()
            context1["message"] =  f"{b.name} added to your order"
        if q == "Salad":
            pedido = Pedido(user=user, name=name, price=price)
            pedido.save()
            context1["message"] = "Added to your order"
            context1["message"] =  f"{b.name} added to your order"
        

        contador = Pedido.objects.all().filter(user=user.id).count()
        context1["contador"] = contador
        


        
        
        print(name)
        print(price)
        print(user.id)
        print(pedido.size)
        
       
        return render(request, "orders/orders2.html", context1,)

def yourOrder(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"contador": "0"})
    else:
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
            pedido2 = Pedido.objects.all().filter(user=user.id).first()
            print(pedido)
            s = request.POST.get("send")
            r = request.POST.get('remove')
            rid = request.POST.get('removeid')
            if s == "send":
                if pedido2 != None:
                    order = Order(user=user, status="Iniciated")
                    order.save()
                    for p in pedido:
                        order.pedidos.add(p)
                    context["Pedido"]= "I"
                    context["order"] = order
                    send_mail('Pinoccios Pizza Order',
                        '<We received your order , it will be ready soon>',
                        'sole.prueba.app@gmail.com',
                        [user.email],
                    )  
                    return render(request, "orders/yourOrder.html", context)
                else:
                    context["message"] = "No orders yet, add some food"
                    return render(request, "orders/yourOrder.html", context)
            if r == "remove":
                p = Pedido.objects.all().filter(id=rid)
                p.delete()
            context["message"] = "Removed"
            contador = Pedido.objects.all().filter(user=user.id).count()
            context["contador"] = contador
            suma = Pedido.objects.all().filter(user=user.id).aggregate(Sum('price'))
            if suma['price__sum'] == None:
                total = "0"
            else:  
                total = float(suma['price__sum'])
            context["total"] = total


            return render(request, "orders/yourOrder.html", context)
            
    
    

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    context3 = {
        "message": "Invalid credentials.",
        "contador": "0"
    }
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("orders"))
    else:
        return render(request, "orders/login.html", context3)

def logout_view(request):
    logout(request)
    context4 = {
    "message": "Logged out.",
    "contador": "0"
    }
    return render(request, "orders/login.html", context4 )



def singup(request):
    if request.method == "GET":
        return render(request, "orders/singup.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        try:
            user_exists = User.objects.get(username=request.POST['username'])
            return render(request, "orders/singup.html", {"message": "Username already exist, try another one"})
        except User.DoesNotExist:
            user = User.objects.create_user(first, email, password)
            user.last_name = last
            user.save()
            return HttpResponseRedirect(reverse("orders"))


