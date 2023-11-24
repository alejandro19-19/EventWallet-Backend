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
from django.conf.urls.static import static
from django.conf import settings

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
    path('core/modify/event',
        views.modify_event, name ='modify_event'),
    path('core/create/invitation',
        views.create_invitation, name = 'create_invitation'),
    path('core/invitation/list',
        views.get_invitations, name ='get_invitations'),
    path('core/invitation/respond',
        views.respond_to_invitation, name='respond_to_invitation'),
    path('core/evento/list',
        views.get_events, name='get_events'),
    path('core/create/activity',
        views.create_activity, name ='create_activity'),
    path('core/invitation/activity',
        views.invitation_activity, name ='create_invitation_activity'),
    path('core/activity/delete',
        views.delete_activity, name = 'delete_activity'),
    path('core/modify/activity',
        views.modify_activity, name = 'modify_activity'),
    path('core/activity/list/<int:pk>/',
        views.get_activities, name = 'get_activities'),
    path('core/event/balances/<int:pk>/',
        views.get_event_balances, name = 'event_balances'),
    path('core/event/contact/delete',
        views.delete_contact_event, name = 'delete_contact_event'),
    path('core/activity/assign/value',
        views.assign_value_activity, name = 'assign_value_activity'),
    path('core/event/participants/list/<int:pk>/',
        views.get_participants_event, name = 'get_participants_event'),
    path('core/activity/participants/list/<int:pk>/',
        views.get_participants_activity, name = 'get_participants_activity'),
    path('core/event/user/balance/<int:event_id>/<int:user_id>/',
        views.get_event_user_balances, name = 'event_user_balances'),
    path('core/event/user/balance/pay/',
        views.pay_balance_event, name = 'pay_balance_event'),     
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)