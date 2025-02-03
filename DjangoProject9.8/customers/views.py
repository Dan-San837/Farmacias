from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ClienteForm
from .models import Cliente

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'customers/lista_clientes.html', {'clientes': clientes})

@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'customers/detalle_cliente.html', {'cliente': cliente})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=nombre).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('customers:crear_cliente')

        usuario = User.objects.create_user(username=nombre, email=email, password=password)
        usuario.save()

        cliente = Cliente.objects.create(
            usuario=usuario,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email
        )
        cliente.save()

        messages.success(request, "Cliente creado exitosamente.")
        return redirect('customers:lista_clientes')

    return render(request, 'customers/formulario_cliente.html')

@login_required
def perfil_cliente(request, cliente_id=None):
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
    else:
        cliente = get_object_or_404(Cliente, usuario=request.user)

    return render(request, 'customers/perfil_cliente.html', {'cliente': cliente})

@login_required
def editar_perfil(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.user != cliente.usuario and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para editar este perfil.")
        return redirect('customers:perfil_cliente_especifico', cliente_id=cliente.id)  # ❌ Estaba mal

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('customers:perfil_cliente_especifico', cliente_id=cliente.id)  # ✅ Ahora está bien
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'customers/edit_perfil.html', {'form': form})

