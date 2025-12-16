from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'mainApp'


router = DefaultRouter()
router.register(r'insumos', views.InsumoView)
router.register(r'pedidos', views.PedidoView)

urlpatterns = [
    #Web
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('solicitar/', views.solicitar_pedido, name='solicitar_pedido'),
    path('exito/', views.pedido_exitoso, name='pedido_exitoso'),
    path('seguimiento/<str:token>/', views.seguimiento_pedido, name='seguimiento_pedido'),

    # Rutas API 
    path('reporte/', views.Reporte, name='reporte_dashboard'),
    path('api/', include(router.urls)),
    path('api/pedidos/filtrar/', views.Pedido_filtrar, name='pedido_filter'),



    #path("employees/", views.employeeView),
    #path("students/", views.student_list),
    #path("students/<int:pk>", views.student_detail)

    #path("students/", views.student_list.as_view()),
    #path("students/<int:pk>", views.student_detail.as_view())
]





    









#router = DefaultRouter()
#router.register("students", views.studentViews)
#urlpatterns =[
    #path("", include(router.urls))
#]


