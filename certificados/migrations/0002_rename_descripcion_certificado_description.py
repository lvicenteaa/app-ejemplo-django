# Generated by Django 4.1.5 on 2023-01-11 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificado',
            old_name='descripcion',
            new_name='description',
        ),
    ]
