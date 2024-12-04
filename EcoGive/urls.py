"""
URL configuration for EcoGive project.

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

#For URL routing with admin and users mapping views

from django.contrib import admin
from django.urls import path
from ecogiveapp import views

urlpatterns = [
    path('admin/', admin.site.urls),    #for admin view
    path('', views.home, name='home'),  #for Homepage view
    path('register/', views.register, name='register'),  #for Registration view
    path('login/', views.user_login, name='login'),      #for Login view
    path('logout/', views.user_logout, name='logout'),   #for Logout view
    path('items/', views.item_list, name='item_list'),   #for Item listing view
    path(
        'items/<int:item_id>/', 
        views.view_item_detail, name='view_item_detail'),  # View Item Detail
    path('items/add/', views.add_item, name='add_item'), #for Add item view
    path(
        'items/<int:item_id>/inquire/', 
        views.inquire_item, name='inquire_item'), #for Inquiry view
    path('dashboard/', views.dashboard, name='dashboard'),  #for User Dashboard view
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),  #for Edit item view
    path(
        'items/<int:item_id>/delete/', 
        views.delete_item, name='delete_item'),  #for Delete item view
]
