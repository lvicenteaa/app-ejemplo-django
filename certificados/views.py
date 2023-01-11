from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CertificadoForm
from .models import Certificado


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # Registrando Usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('certificados')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden'
        })


def certificados(request):
    certificados = Certificado.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'certificados.html', {
        'certificados': certificados
    })

def create_certificado(request):
    if request.method == 'GET':
        return render(request, 'created_certificado.html', {
            'form': CertificadoForm
        })
    elif request.method == 'POST':
        try:
            form = CertificadoForm(request.POST)
            new_certificado = form.save(commit=False)
            new_certificado.user = request.user
            new_certificado.save()
            return redirect('certificados')
        except ValueError:
            return render(request, 'create_certificado.html', {
                'form': CertificadoForm,
                'error': 'No hay datos'
            })

def certificado_detalle(request, certificado_id):
    if request.method == 'GET':
        certificado = get_object_or_404(Certificado, pk=certificado_id, user=request.user)
        form = CertificadoForm(instance=certificado)
        return render(request, 'certificado_detalle.html', {
            'certificado': certificado,
            'form': form
        })
    elif request.method == 'POST':
        try:
            certificado = get_object_or_404(Certificado, pk=certificado_id, user=request.user)
            form = CertificadoForm(request.POST, instance=certificado)
            form.save()
            return redirect('certificados')
        except ValueError:
            return render(request, 'certificado_detalle.html', {
                'certificado': certificado,
                'form': form,
                'error': 'Error actualizando Certificado'
            })

def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('certificados')
