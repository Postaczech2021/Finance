from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.manage_categories,name='manage_categories'), # 
    path('add_income/', views.add_income, name='add_income'),
    path('add_outcome/', views.add_outcome, name='add_outcome'),
    path('edit_income/<int:income_id>',views.edit_income,name='edit_income'),
    path('edit_outcome/<int:outcome_id>', views.edit_outcome, name='edit_outcome'),
    path('delete_income/<int:income_id>',views.delete_income,name='delete_income'),
    path('delete_outcome/<int:outcome_id>',views.delete_outcome,name='delete_outcome'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('list/', views.list_transactions, name='list_transactions'),
]
