from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido, ImagenReferencia
from django.utils.html import format_html


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields= ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "mostrar_imagen", "categoria", "precio_base")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria",)

    
    def mostrar_imagen(self, obj):
        if obj.imagen1:
            
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.imagen1.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Portada"



@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "cantidad", "unidad", "marca", "color")
    search_fields = ("nombre", "tipo", "marca")
    list_filter = ("tipo",)
    list_editable = ("cantidad",)

class ImagenReferenciaInline(admin.TabularInline):
    model = ImagenReferencia
    extra = 1 


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "cliente_nombre", 
        "producto_referencia",
        "estado_pedido", 
        "estado_pago", 
        "plataforma", 
        "fecha_solicitada"
    )
    search_fields = ("cliente_nombre", "email", "id", "token")
    list_filter = ("estado_pedido", "estado_pago", "plataforma", "fecha_creacion")
    
    inlines = [ImagenReferenciaInline]
    
    readonly_fields = ("token", "fecha_creacion")
    
    
    fieldsets = (
        ("Información del Cliente", {
            "fields": ("cliente_nombre", "email", "telefono", "red_social")
        }),
        ("Detalles del Pedido", {
            "fields": ("producto_referencia", "descripcion_solicitud", "fecha_solicitada")
        }),
        ("Estado y Seguimiento", {
            "fields": ("estado_pedido", "estado_pago", "plataforma", "token", "fecha_creacion")
        }),
    )