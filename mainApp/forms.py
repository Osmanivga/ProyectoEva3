from django import forms
from .models import Pedido, ImagenReferencia

class SolicitudPedidoForm(forms.ModelForm):
    # Campos extra
    imagen_ref_1 = forms.ImageField(required=False, label="Imagen de referencia 1")
    imagen_ref_2 = forms.ImageField(required=False, label="Imagen de referencia 2")
    imagen_ref_3 = forms.ImageField(required=False, label="Imagen de referencia 3")

    otra_plataforma = forms.CharField(
        required=False,
        label="¿Cuál?",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique...'})
    )

    class Meta:
        model = Pedido
        # Campos exactos de tu modelo
        fields = [
            'cliente_nombre', 'email', 'telefono', 'red_social',
            'producto_referencia', 'descripcion_solicitud', 'fecha_solicitada',
            'plataforma'
        ]
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'red_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'producto_referencia': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_solicitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe tu idea...'}),
            'fecha_solicitada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'plataforma': forms.Select(attrs={'class': 'form-select', 'id': 'select-plataforma'}),
        }

    def save(self, commit=True):
        pedido = super().save(commit=False)

        if self.cleaned_data.get('plataforma') == 'OTRO':
            pass 
        
        if commit:
            pedido.save()
            # Guardar imágenes
            imagenes = [
                self.cleaned_data.get('imagen_ref_1'),
                self.cleaned_data.get('imagen_ref_2'),
                self.cleaned_data.get('imagen_ref_3')
            ]
            for img in imagenes:
                if img:
                    ImagenReferencia.objects.create(pedido=pedido, imagen=img)
        
        return pedido