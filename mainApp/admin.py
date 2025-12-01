from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido, ImagenReferencia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields= ("nombre",)
