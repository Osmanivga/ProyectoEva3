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


