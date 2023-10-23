"""
URL configuration for Event_Wallet_Backend project.

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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/create',
        views.CreateUserAdminView.as_view(), name='create_user'),
    path('core/login',
        views.CreateTokenView.as_view(), name='login_user'),
    path('core/modify',
        views.ManageUserView.as_view(), name='modify_user'),
    path('core/contacto',
        views.create_contact, name = 'create_contact'),
    path('core/modify/password',
        views.modify_password, name = 'modify_user_password'),
    path('core/deactivate',
        views.deactivate_account, name = 'deactivate_user_account'),
    path('core/contacto/list',
        views.get_contacts, name = 'get_contacts'),
    path('core/contacto/delete',
        views.delete_contact, name = 'delete_contact'),
    path('core/create/event',
        views.create_event, name ='create_event'),
       
]
