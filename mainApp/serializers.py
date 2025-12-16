from rest_framework import serializers
from .models import employee
from .models import estudiante
from .models import Insumo, Pedido




class InsumoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = "__all__"

class PedidoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"





# --- EJERCICIOS
class employeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = "__all__"


class estudianteSerializers(serializers.ModelSerializer):
    class Meta:
        model = estudiante
        fields = "__all__"


