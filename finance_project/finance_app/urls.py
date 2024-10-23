from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.manage_categories,name='manage_categories'), # 
    path('add_income/', views.add_income, name='add_income'),
    path('add_outcome/', views.add_outcome, name='add_outcome'),
    path('edit_income/<int:income_id>',views.edit_income,name='edit_income'),
    path('list/', views.list_transactions, name='list_transactions'),
]
