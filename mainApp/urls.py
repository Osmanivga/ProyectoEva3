from django.urls import path
from . import views
from mainApp import views

app_name = 'mainApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('solicitar/', views.solicitar_pedido, name='solicitar_pedido'),
    path('exito/', views.pedido_exitoso, name='pedido_exitoso'),
    path('seguimiento/<str:token>/', views.seguimiento_pedido, name='seguimiento_pedido'),
    path("employees/", views.employeeView),
    path("students/", views.student_list),
    path("students/<int:pk>", views.student_detail)
]


