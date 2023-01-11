from django.contrib import admin
from .models import Certificado

class CertificadoAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
# Register your models here.
admin.site.register(Certificado, CertificadoAdmin)