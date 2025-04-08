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
   path('requirements/', views.requirements_dashboard, name='requirements_dashboard'),
 
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('service/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('service/edit/<int:pk>/', views.edit_service, name='edit_service'),
    
]