from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from .models import Menu, Order, Paycheck
from .forms import SignUpForm
from decimal import Decimal

from django.contrib.auth.decorators import login_required


# Create your views here.


def customer(request):
    return render(request, 'customerportal.html')


def login_user(request):
    if request.user.is_authenticated:
        return render(request, 'coffeshop')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('coffeeshop')  # profile
        else:
            msg = 'Error Login'
            print(msg)
            form = AuthenticationForm(request.POST)
            return render(request, 'login_signup.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login_signup.html', {'form': form})

    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('coffeeshop')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
    
    
    

def logout_user(request):
    logout(request)
    return redirect('homepage')

def homepage(request):
    return render(request, 'index.html')





def add_to_cart(request, item_id):
    item = Menu.objects.get(pk=item_id)
    
    # Check if the item is already in the user's cart
    cart_item, created = Order.objects.get_or_create(
        customer=request.user, items=item, defaults={'quantity': 1, 'price': item.price})
    
    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def view_cart(request):
    cart_items = Order.objects.filter(customer=request.user)
    grand_total_cart_price = sum(
        item.items.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'grand_total_cart_price': grand_total_cart_price})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)
    cart_item.delete()

    if Order.objects.filter(customer=request.user).count() == 0:
        messages.info(request, "Your cart is now empty.")
        return redirect('menu')

    return redirect('cart')

def reduce_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)

    # If the quantity is more than 0, reduce it
    if cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.warning(request, "The quantity cannot be reduced further.")

    return redirect('cart')

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

def clear_cart(request):
    cart_items = Order.objects.filter(customer=request.user)
    cart_items.delete()
    return redirect('menu')

def checkout(request):
    cart_items = Order.objects.filter(customer=request.user)

    # Clear the cart after checkout
    cart_items.delete()

    return redirect('menu')

def searchMenu(request):
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(nameicontains=searched)

        return render(request,'searchMenu.html',
    {'searched':searched,
     'menuResult':menuResult})
    else:
        return render(request,'searchMenu.html',
    {} )

def userSearchMenu(request):
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(nameicontains=searched)

        return render(request,'userSearchMenu.html' ,
    {'searched':searched,
     'menuResult':menuResult})
    else:
        return render(request,'userSearchMenu.html' ,
    {})

def menu(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
#Fetch all products (items) or apply any filtering you need here
    items = Menu.objects.all()


    print('you are : ', request.session.get('email'))
    return render(request, 'menu.html', {'items': items})

def viewmenu(request):
    item_list = Menu.objects.all()
    return render(request, 'viewmenu.html', {'item_list': item_list})

def all_orders(request):
    order_list = Order.objects.all()
    return render(request, 'staffportal.html', {"order_list" : order_list})

@login_required
def accept_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        # Calculate the total cost for the accepted item
        total_cost = order.price * order.quantity

        # Create or update the Paycheck entry for the staff
        staff = request.user
        paycheck, created = Paycheck.objects.get_or_create(staff=staff)
        paycheck.total_cost += total_cost * Decimal('0.15')  # 15% of the total cost
        paycheck.save()

        # Delete the accepted order
        order.delete()

        messages.success(request, 'Order accepted')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')

    return redirect('staffportal') 

@login_required
def decline_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, 'Order declined')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')

    return redirect('staffportal')

@login_required
def view_earnings(request):
    staff = request.user
    paycheck = Paycheck.objects.filter(staff=staff).first()

    total_earnings = paycheck.total_cost if paycheck else 0.0

    return render(request, 'paycheck.html', {'total_earnings': total_earnings})