from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Pedido
from .forms import SolicitudPedidoForm

# --- Vistas Públicas ---

def index(request):
    
    productos_destacados = Producto.objects.all()[:6]
    return render(request, 'mainApp/index.html', {
        'productos_destacados': productos_destacados
    })

def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id and categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)
    
    return render(request, 'mainApp/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if categoria_id and categoria_id.isdigit() else None
    })

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'mainApp/detalle_producto.html', {
        'producto': producto
    })

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
            # Guardamos el token en sesión para la página de éxito
            request.session['nuevo_token'] = str(pedido.token)
            return redirect('pedido_exitoso')
    else:
        form = SolicitudPedidoForm(initial={'producto_referencia': producto_inicial})

    return render(request, 'mainApp/solicitar_pedido.html', {'form': form})

def pedido_exitoso(request):
    token = request.session.get('nuevo_token')
    if not token:
        return redirect('index')
    
    # Buscamos por el campo 'token'
    pedido = get_object_or_404(Pedido, token=token)
    
    return render(request, 'mainApp/pedido_exitoso.html', {
        'pedido': pedido,
    })

def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    imagenes = pedido.imagenes_referencia.all()
    
    return render(request, 'mainApp/seguimiento_pedido.html', {
        'pedido': pedido,
        'imagenes_referencia': imagenes
    })