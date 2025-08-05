from django.urls import path
from . import views

app_name = 'calculator_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('standard/', views.standard_calculator_view, name='standard_calculator'),
    path('interest/', views.interest_calculator_view, name='interest_calculator'),
    path('installment/', views.installment_calculator_view, name='installment_calculator')
]
