from django import forms
from .models import Pedido, ImagenReferencia

class SolicitudPedidoForm(forms.ModelForm):
    # Campos "extra" para subir hasta 3 imágenes de referencia
    imagen_ref_1 = forms.ImageField(required=False, label="Imagen de referencia 1")
    imagen_ref_2 = forms.ImageField(required=False, label="Imagen de referencia 2")
    imagen_ref_3 = forms.ImageField(required=False, label="Imagen de referencia 3")

    otra_plataforma = forms.CharField(
        required=False,
        label="¿Cuál?",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especifique la plataforma...'})
    )

    class Meta:
        model = Pedido
        # Usamos tus nombres de campo exactos
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
            'descripcion_solicitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe colores, textos, ubicación de logos, etc.'}),
            'fecha_solicitada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'plataforma': forms.Select(attrs={'class': 'form-select', 'id': 'select-plataforma'}),
        }

    def save(self, commit=True):
        # 1. Instanciamos el pedido sin guardar en BD aún
        pedido = super().save(commit=False)

        # 2. Lógica para "Otra plataforma" (opcional, por ahora solo pasamos)
        if self.cleaned_data.get('plataforma') == 'OTRO':
            pass 
        
        if commit:
            pedido.save()
            # 3. Guardar las imágenes de referencia manuales
            imagenes = [
                self.cleaned_data.get('imagen_ref_1'),
                self.cleaned_data.get('imagen_ref_2'),
                self.cleaned_data.get('imagen_ref_3')
            ]
            for img in imagenes:
                if img:
                    ImagenReferencia.objects.create(
                        pedido=pedido, 
                        imagen=img
                    )
        
        return pedido