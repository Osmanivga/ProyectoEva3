from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido
from .forms import SolicitudPedidoForm
from django.http import JsonResponse
from .models import employee
from rest_framework .decorators import api_view
from .models import estudiante
from rest_framework.response import Response
from .serializers import estudianteSerializers
from rest_framework import status

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






def employeeView(request):
    empledados = employee.objects.all()
    data= {"employees": list(empledados.values("name", "salary"))}
 
    return JsonResponse(data)


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