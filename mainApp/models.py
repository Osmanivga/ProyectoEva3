from django.db import models
import uuid  # token único 


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_base = models.IntegerField()  # Usamos Integer para pesos chilenos (sin decimales)
    
 
    imagen1 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre




class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50) # Ej: Polera, Tinta, Filamento
    cantidad = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, blank=True, null=True) # Ej: Metros, Unidades, Litros
    marca = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"



class Pedido(models.Model):
    #  campos de selección
    
    ESTADOS_PEDIDO = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('EN_PROCESO', 'En proceso'),
        ('REALIZADA', 'Realizada'),
        ('ENTREGADA', 'Entregada'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    ESTADOS_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
    ]

    PLATAFORMAS = [
        ('WEB', 'Sitio Web'),
        ('FB', 'Facebook'),
        ('IG', 'Instagram'),
        ('WSP', 'WhatsApp'),
        ('PRESENCIAL', 'Presencial'),
        ('OTRO', 'Otro'),
    ]

    # Datos del Cliente
    cliente_nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    red_social = models.CharField(max_length=100, blank=True)
    
    # Datos del Pedido
    producto_referencia = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_solicitud = models.TextField()
    fecha_solicitada = models.DateField(null=True, blank=True)
    
    # Datos Administrativos
    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, default='WEB')
    estado_pedido = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='SOLICITADO')
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='PENDIENTE')
    
    # Token único para seguimiento (Se genera solo)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"
    
    

class ImagenReferencia(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='imagenes_referencia', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='referencias_clientes/')

    def __str__(self):
        return f"Imagen para pedido {self.pedido.id}"
