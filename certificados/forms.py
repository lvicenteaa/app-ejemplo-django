from django.forms import ModelForm
from .models import Certificado

class CertificadoForm(ModelForm):
    class Meta:
        model = Certificado
        fields = ['title', 'description', 'company']