from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('income/', views.income_list, name='income_list'),
    path('income/create/', views.create_income, name='create_income'),
    path('income/edit/<int:id>/', views.edit_income, name='edit_income'),
    path('expense/', views.expense_list, name='expense_list'),
    path('expense/create/', views.create_expense, name='create_expense'),
    path('expense/category/', views.expense_category_list,
         name='expense_category_list'),
    path('expense/category/create/', views.create_expense_category,
         name='create_expense_category'),
    path('get_months/', views.get_months, name='get_months'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),

]
