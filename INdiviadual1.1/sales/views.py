from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from customers.models import Cliente
from .forms import PedidoForm
from inventory.models import Sucursal, Medicamento #MedicamentoDescrip
from .models import Pedido, DetallePedido



def ventas_index(request):
    pedidos = Pedido.objects.all()  # Filtra según las reglas de tu sistema
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/index.html', {'pedidos': pedidos, 'sucursales': sucursales})

def index(request):
    """Página principal del módulo de ventas."""
    return render(request, 'sales/index.html')


def ventas_list(request):
    sucursal_id = request.GET.get('sucursal')
    ventas = Pedido.objects.all()
    if sucursal_id and sucursal_id.isdigit():  # Si hay un filtro de sucursal
        ventas = Pedido.objects.filter(sucursal_origen_id=sucursal_id)

    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales para el filtro
    return render(request, 'sales/ventas_list.html', {"ventas": ventas, "sucursales": sucursales})


def pedido_detalle(request, pedido_id):
    """Muestra el detalle de un pedido específico."""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'sales/pedido_detalle.html', {'pedido': pedido})


@login_required
def realizar_venta(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    medicamentos = Medicamento.objects.filter(sucursal=sucursal)

    # Verificar si el usuario tiene un cliente asociado
    try:
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        # Mostrar un error o redirigir si el usuario no tiene un cliente asociado
        error = "Debe ser un cliente registrado para realizar una compra. Complete su perfil primero."
        return render(request, "sales/realizar_venta.html", {
            "sucursal": sucursal,
            "medicamentos": medicamentos,
            "error": error
        })

    if request.method == "POST":
        medicamento_id = request.POST.get("medicamento_id")
        cantidad = int(request.POST.get("cantidad"))
        medicamento = get_object_or_404(Medicamento, id=medicamento_id, sucursal=sucursal)

        if medicamento.stock >= cantidad:
            total = medicamento.precio * cantidad
            # Crear el pedido con el cliente asociado
            pedido = Pedido.objects.create(
                cliente=cliente,
                sucursal_origen=sucursal,
                estado="pendiente",
                total=total
            )
            DetallePedido.objects.create(
                pedido=pedido,
                medicamento=medicamento,
                cantidad=cantidad,
                subtotal=total
            )
            # Actualizar el stock del medicamento
            medicamento.stock -= cantidad
            medicamento.save()
            return HttpResponseRedirect(reverse("sales:ventas_list"))
        else:
            error = f"Stock insuficiente para {medicamento.nombre}. Solo hay {medicamento.stock} disponibles."
            return render(request, "sales/realizar_venta.html", {
                "sucursal": sucursal,
                "medicamentos": medicamentos,
                "error": error
            })

    return render(request, "sales/realizar_venta.html", {
        "sucursal": sucursal,
        "medicamentos": medicamentos,
    })


def seguimiento(request):
    """Seguimiento de pedidos (mostrar el estado y progreso)."""
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-fecha')
    return render(request, 'sales/seguimiento.html', {'pedidos': pedidos})


def seleccionar_sucursal(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/seleccionar_sucursal.html', {'sucursales': sucursales})


def calcular_total_pedido():
    # ODO document why this method is empty
    pass


def crear_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales:seguimiento')

    else:
        form = PedidoForm()

    return render(request, 'sales/crear_pedido.html', {
        'form': form,
    })


def medicamentos_list(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'sales/medicamentos_list.html', {'medicamentos': medicamentos})


def actualizar_estado (request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
    return redirect('sales:seguimiento')

