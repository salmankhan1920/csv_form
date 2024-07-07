from django.urls import path
from . import views

urlpatterns = [
   path('', views.order_form, name='order_form'),

    path('order/', views.order_form, name='order_form'),
    path('display-csv/', views.display_csv, name='display_csv'),
    path('download-csv/', views.download_csv, name='download_csv'),
     path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('logs/', views.user_logs, name='user_logs'),
      path('all-user-logs/', views.all_user_logs, name='all_user_logs'),
      path('user-count/', views.user_count, name='user_count'),
]

    





