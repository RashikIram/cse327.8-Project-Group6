"""
URL configuration for Coffee_Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Coffee_Shop_Management import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('coffeeshop', views.customer, name='coffeeshop'),
    path('sign_in', views.login_user, name='sign_in'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('menu', views.menu, name='menu'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('managerportal', views.manager, name='manager'),
    path('managestaff', views.manage_staff, name='manage_staff'),
    path('managemenu', views.manage_menu, name='manage_menu'),
    path('staffportal', views.staff, name='staff'),
    path('view_menu', views.viewmenu, name='view_menu'),
    path('searchMenu', views.searchMenu, name='searchMenu'),
    

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
