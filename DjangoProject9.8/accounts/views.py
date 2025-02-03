from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm
from .models import Cliente, EmpleadoSucursal
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Manejar el rol
            rol = form.cleaned_data['rol']
            if rol == 'cliente':
                Cliente.objects.create(usuario=user)
            elif rol == 'empleado':
                sucursal = form.cleaned_data.get('sucursal')
                EmpleadoSucursal.objects.create(usuario=user, sucursal=sucursal)

            return redirect('accounts:login')
    else:
        form = RegistroForm()

    return render(request, 'accounts/register.html', {'form': form})

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso."),
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Inténtalo de nuevo.")

    return render(request, "accounts/login.html")