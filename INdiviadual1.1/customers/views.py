from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.models import User
from django.contrib import messages

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
        print(request.POST)  # Imprime los datos enviados
        # Obtén los datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')

        # Crear un usuario temporal para asociarlo al cliente
        usuario = User.objects.create(username=nombre, email=email)
        usuario.save()

        # Crear el cliente
        cliente = Cliente.objects.create(
            usuario=usuario,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email
        )
        cliente.save()

        # Redirigir a la lista de clientes
        return redirect('customers:lista_clientes')

    return render(request, 'customers/formulario_cliente.html')

def index(request):
    return render(request, 'customers/index.html')

def perfil_cliente(request, cliente_id):
    try:
        # Recupera el cliente con el ID pasado por la URL
        cliente = get_object_or_404(Cliente, id=cliente_id)
        return render(request, 'customers/perfil_cliente.html', {'cliente': cliente})
    except AttributeError:
        return redirect ('index')