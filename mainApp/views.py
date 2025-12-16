from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido
from .forms import SolicitudPedidoForm
from django.http import JsonResponse
from .models import employee
from rest_framework .decorators import api_view
from .models import estudiante, Insumo, Pedido
from rest_framework.response import Response
from .serializers import estudianteSerializers, InsumoSerializers, PedidoSerializers
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import viewsets
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count


class InsumoView(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializers



class PedidoView(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializers

@api_view(["GET"])
def Pedido_filtrar(request):
    pedidos = Pedido.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    estado = request.GET.get('estado')
    limite = request.GET.get('limite')

    if fecha_inicio and fecha_fin:
        try:
            pedidos =pedidos.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        except: return Response({"error": "Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    if estado:
        pedidos = pedidos.filter(estado_pedido=estado)
    
    if limite:
        try:
            pedidos = pedidos[:int(limite)]
        except ValueError:
            pass

    serializer = PedidoSerializers(pedidos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def Reporte(request):
    pedidos_por_estado = Pedido.objects.values('estado_pedido').annotate(total=Count('id'))
    pedidos_por_plataforma = Pedido.objects.values('plataforma').annotate(total=Count('id'))
    productos_top = Pedido.objects.values('producto_referencia__nombre').annotate(total=Count('id')).order_by('-total')[:5]

    return render(request, 'mainApp/reporte.html', {
        'pedidos_estado': list(pedidos_por_estado),
        'pedidos_plataforma': list(pedidos_por_plataforma),
        'productos_top': list(productos_top)
    })







# --------------Ejercicio Estudiante viwesets---------------->
'''
class studentViews(viewsets.ModelViewSet):
    queryset = estudiante.objects.all()
    serializer_class = estudianteSerializers


'''

# --------------Ejercicio Estudiante mixins---------------->
'''
class student_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = estudiante.objects.all()
    serializer_class = estudianteSerializers

    def get(self, request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

class student_detail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = estudiante.objects.all()
    serializer_class = estudianteSerializers

    def get(self, request, pk):
        return self.retrieve(request)
    
    def put(self,request, pk):
        return self.update(request)
    
    def delete(self,request, pk):
        return self.destroy(request)
    
'''

# --------------Ejercicio estudiante simple---------------->
'''

@api_view(["GET", "POST"])
def student_list(request):
    if request.method == "GET":
        students = estudiante.objects.all()
        ser = estudianteSerializers(students, many=True)
        return Response(ser.data)
    
    if request.method == "POST":
        ser = estudianteSerializers(data = request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def student_detail(request, pk):
    try:
        student = estudiante.objects.get(pk=pk)
    except:
        return Response( status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        ser= estudianteSerializers(student)
        return Response(ser.data)
    
    if request.method == "PUT":
        ser = estudianteSerializers(student, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



    if request.method == "DELETE":
        student.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)

'''

# --------------Ejercicio Empleados Api---------------->
'''
def employeeView(request):
    empledados = employee.objects.all()
    data= {"employees": list(empledados.values("name", "salary"))}
 
    return JsonResponse(data)

'''



# -------------------------EVA PART 1---------------->

def index(request):
    # Mostramos todos los productos (primeros 6)
    productos_destacados = Producto.objects.all()[:6]
    return render(request, 'mainApp/index.html', {
        'productos_destacados': productos_destacados
    })

def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id and categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)
        categoria_actual = int(categoria_id)
    else:
        categoria_actual = None
    
    return render(request, 'mainApp/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_actual
    })

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'mainApp/detalle_producto.html', {'producto': producto})

def solicitar_pedido(request):
    producto_inicial = None
    if 'producto' in request.GET:
        prod_id = request.GET.get('producto')
        if prod_id and prod_id.isdigit():
            producto_inicial = get_object_or_404(Producto, pk=prod_id)

    if request.method == 'POST':
        form = SolicitudPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save()
            request.session['nuevo_token'] = str(pedido.token)
            return redirect('mainApp:pedido_exitoso')
    else:
        form = SolicitudPedidoForm(initial={'producto_referencia': producto_inicial})

    return render(request, 'mainApp/solicitar_pedido.html', {'form': form})

def pedido_exitoso(request):
    token = request.session.get('nuevo_token')
    if not token:
        return redirect('mainApp:index')
    
    try:
        pedido = Pedido.objects.get(token=token)
    except Pedido.DoesNotExist:
        return redirect('mainApp:index')
    
    return render(request, 'mainApp/pedido_exitoso.html', {'pedido': pedido})

def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    imagenes = pedido.imagenes_referencia.all()
    
    return render(request, 'mainApp/seguimiento_pedido.html', {
        'pedido': pedido, 
        'imagenes_referencia': imagenes
    })

