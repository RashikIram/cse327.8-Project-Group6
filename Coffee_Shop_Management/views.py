from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from .models import Menu
from .forms import SignUpForm


# Create your views here.


def customer(request):
    return render(request, 'customerportal.html')

def login_user(request):
    #Check to see if logging in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(request, 'coffeeshop')
    else:  
        return render(request, 'login_signup.html')
    
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('coffeeshop')
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form':form})

	return render(request, 'signup.html', {'form':form})
    
    
    

def logout_user(request):
    logout(request)
    return redirect('homepage')

def homepage(request):
    return render(request, 'index.html')

def menu(request):
    item_list = Menu.objects.all()
    return render(request, 'menu.html', {'item_list':item_list})

def staff(request):
    return render(request, 'staffportal.html')

def manager(request):
    return render(request, 'managerPortalMain.html')

def manage_menu(request):
    return render(request, 'managerPortalMenu.html')

def manage_staff(request):
    return render(request, 'managerPortalStaff.html')

def viewmenu(request):
    item_list = Menu.objects.all()
    return render(request, 'viewmenu.html', {'item_list': item_list})

def searchMenu(request):
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(item_name__icontains=searched)

        return render(request,'searchMenu.html',
    {'searched':searched,
     'menuResult':menuResult})
    else:
        return render(request,'searchMenu.html',
    {})

def userSearchMenu(request):
    if request.method == "POST":
        searched = request.POST['searched']
        menuResult = Menu.objects.filter(item_name__icontains=searched)

        return render(request,'userSearchMenu.html',
    {'searched':searched,
     'menuResult':menuResult})
    else:
        return render(request,'userSearchMenu.html',
    {})

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')