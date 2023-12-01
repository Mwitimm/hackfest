from django.urls import path

from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot/', views.forgot_password, name='forgot'),
    path('logout/', views.logout_user, name='log_out'),
    path('loans/', views.loans, name='loans'),
    path('notification/<str:sender>/<int:id>', views.notification, name='notification'),
    path('delete/<uuid:id>', views.delete, name='delete'),
    path('rent/<uuid:id>', views.rent, name='rent'),
    path('logs/', views.logs, name='logs'),
   
   

    
]
