from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from .models import Menu, Order, Paycheck
from .forms import SignUpForm
from decimal import Decimal

from django.contrib.auth.decorators import login_required

def customer(request):
    """
    This function displays the customer portal page.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page for the customer portal.

    :rtype: HttpResponse.
    """
    return render(request, 'customerportal.html')

def login_user(request):
    """
    This function is used to log in the user and redirect to the appropriate page based on user type.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Redirect to staff portal or coffee shop profile if login is successful, 
             otherwise show an error message.

    :rtype: HttpResponse.
    """
    if request.user.is_authenticated:
        return render(request, 'coffeshop')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staffportal')
            else:
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
    """
    This function creates a new user and redirect to the coffee shop profile.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Redirect to the coffee shop profile page after successful signup.

    :rtype: HttpResponse.
    """
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
    """
    This function is used to log out the user and redirect to the homepage.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Redirect to the homepage after successful logout.

    :rtype: HttpResponse.
    """
    logout(request)
    return redirect('homepage')

def homepage(request):
    """
    This function displays the homepage.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page for the homepage.

    :rtype: HttpResponse.
    """
    return render(request, 'index.html')

def add_to_cart(request, item_id):
    """
    This function is used to add an item to the user's cart from menu.

    :param request: HttpRequest from the user.
    :param item_id: The ID of the item to be added to the cart.

    :type request: HttpRequest.
    :type item_id: int.

    :return: Redirect to the cart page.

    :rtype: HttpResponse.
    """
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
    """
    This function is used to view the user's shopping cart.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing the user's cart and its total price.

    :rtype: HttpResponse.
    """
    cart_items = Order.objects.filter(customer=request.user)
    grand_total_cart_price = sum(
        item.items.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'grand_total_cart_price': grand_total_cart_price})

def remove_from_cart(request, cart_item_id):
    """
    This function is used to remove an item from the user's shopping cart.

    :param request: HttpRequest from the user.
    :param cart_item_id: The ID of the item to be removed from the cart.

    :type request: HttpRequest.
    :type cart_item_id: int.

    :return: Redirect to the cart or menu page.

    :rtype: HttpResponse.
    """
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)
    cart_item.delete()

    if Order.objects.filter(customer=request.user).count() == 0:
        messages.info(request, "Your cart is now empty.")
        return redirect('menu')

    return redirect('cart')

def reduce_quantity(request, cart_item_id):
    """
    This function is used to reduce the quantity of an item in the user's shopping cart.

    :param request: HttpRequest from the user.
    :param cart_item_id: The ID of the item whose quantity is to be reduced.

    :type request: HttpRequest.
    :type cart_item_id: int.

    :return: Redirect to the cart page.

    :rtype: HttpResponse.
    """
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)

    # If the quantity is more than 0, reduce it
    if cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.warning(request, "The quantity cannot be reduced further.")

    return redirect('cart')

def increase_quantity(request, cart_item_id):
    """
    This function is used to increase the quantity of an item in the user's shopping cart.

    :param request: HttpRequest from the user.
    :param cart_item_id: The ID of the item whose quantity is to be increased.

    :type request: HttpRequest.
    :type cart_item_id: int.

    :return: Redirect to the cart page.

    :rtype: HttpResponse.
    """
    cart_item = get_object_or_404(Order, pk=cart_item_id, customer=request.user)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

def clear_cart(request):
    """
    This function is used to clear all items from the user's shopping cart.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Redirect to the menu page.

    :rtype: HttpResponse.
    """
    cart_items = Order.objects.filter(customer=request.user)
    cart_items.delete()
    return redirect('menu')

def checkout(request):
    """
    This function is used to checkout the items in the user's shopping cart and clear the cart.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Redirect to the menu page after successful checkout.

    :rtype: HttpResponse.
    """
    cart_items = Order.objects.filter(customer=request.user)

    # Clear the cart after checkout
    cart_items.delete()

    return redirect('menu')

def search_menu(request):
    """
    This function is used to search for items in the menu.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing search results.

    :rtype: HttpResponse.
    """
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(name__icontains=searched)

        return render(request, 'searchMenu.html', {'searched': searched, 'menuResult': menuResult})
    else:
        return render(request, 'searchMenu.html', {})

def user_search_menu(request):
    """
    This function is used to search for items in the menu for a user.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing search results for the user.

    :rtype: HttpResponse.
    """
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(name__icontains=searched)

        return render(request, 'userSearchMenu.html', {'searched': searched, 'menuResult': menuResult})
    else:
        return render(request, 'userSearchMenu.html', {})

def menu(request):
    """
    This function is used to display the menu page.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing the menu.

    :rtype: HttpResponse.
    """
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    # Fetch all products (items) or apply any filtering you need here
    items = Menu.objects.all()

    print('you are: ', request.session.get('email'))
    return render(request, 'menu.html', {'items': items})

def viewmenu(request):
    """
    This function is used to View the menu for everyone.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing the menu for everyone.

    :rtype: HttpResponse.
    """
    item_list = Menu.objects.all()
    return render(request, 'viewmenu.html', {'item_list': item_list})

def all_orders(request):
    """
    This function is used to display all orders for staff.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing all orders for staff.

    :rtype: HttpResponse.
    """
    order_list = Order.objects.all()
    return render(request, 'staffportal.html', {"order_list": order_list})

from decimal import Decimal

@login_required
def accept_order(request, order_id):
    """
    This function is used to accept an order and calculate earnings for the staff.

    :param request: HttpRequest from the user.
    :param order_id: The ID of the order to be accepted.

    :type request: HttpRequest.
    :type order_id: int.

    :return: Redirect to the staff portal after accepting the order.

    :rtype: HttpResponse.
    """
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
    """
    This function is used to decline an order.

    :param request: HttpRequest from the user.
    :param order_id: The ID of the order to be declined.

    :type request: HttpRequest.
    :type order_id: int.

    :return: Redirect to the staff portal after declining the order.

    :rtype: HttpResponse.
    """
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, 'Order declined')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')

    return redirect('staffportal')

@login_required
def view_earnings(request):
    """
    This function is used to view earnings for the staff.

    :param request: HttpRequest from the user.

    :type request: HttpRequest.

    :return: Rendered HTML page showing earnings for the staff.

    :rtype: HttpResponse.
    """
    staff = request.user
    paycheck = Paycheck.objects.filter(staff=staff).first()

    total_earnings = paycheck.total_cost if paycheck else 0.0

    return render(request, 'paycheck.html', {'total_earnings': total_earnings})
