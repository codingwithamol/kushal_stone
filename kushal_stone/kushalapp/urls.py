from . import views
from django.urls import path # type: ignore

urlpatterns = [
   path('', views.index, name='index'),
   path('signup/', views.signup, name='signup'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard'),
   path('operations_dashboard/', views.operations_dashboard, name='operations_dashboard'),
   path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
   path('finance_dashboard/', views.finance_dashboard, name='finance_dashboard'),
   path('create_user/', views.create_user, name='create_user'), 
    
]