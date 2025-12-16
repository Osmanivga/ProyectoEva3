from rest_framework import serializers
from .models import employee
from .models import estudiante

class employeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = "__all__"


class estudianteSerializers(serializers.ModelSerializer):
    class Meta:
        model = estudiante
        fields = "__all__"


