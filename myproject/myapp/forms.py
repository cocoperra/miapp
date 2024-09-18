from django import forms
from .models import Player, Pdf
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm

# Formulario para el modelo de Player
class CoverImageForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['cover_image']
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nombre', 'equipo', 'categoria', 'ano', 'posicion',  'cover_image']  # Corregido

# Formulario para el modelo de PDF
class PDFForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['file']
PDFFormSet = inlineformset_factory(Player, Pdf, form=PDFForm, extra=1, can_delete=True)