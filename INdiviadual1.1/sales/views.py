from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoFormSet
from inventory.models import Sucursal, Medicamento


def ventas_index(request):
    pedidos = Pedido.objects.all()  # Filtra según las reglas de tu sistema
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/index.html', {'pedidos': pedidos, 'sucursales': sucursales})

def index(request):
    """Página principal del módulo de ventas."""
    return render(request, 'sales/index.html')


def ventas_list(request):
    """Lista de todas las ventas."""
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'sales/ventas_list.html', {'pedidos': pedidos})


def pedido_detalle(request, pedido_id):
    """Muestra el detalle de un pedido específico."""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'sales/pedido_detalle.html', {'pedido': pedido})


def realizar_venta(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    medicamentos = Medicamento.objects.filter(sucursal=sucursal)

    if request.method == "POST":
        medicamento_id = request.POST.get("medicamento_id")
        cantidad = int(request.POST.get("cantidad"))
        medicamento = get_object_or_404(Medicamento, id=medicamento_id, sucursal=sucursal)

        if medicamento.stock >= cantidad:
            total = medicamento.precio * cantidad
            # Crear un nuevo pedido
            pedido = Pedido.objects.create(
                cliente=request.user.cliente,  # Suponiendo que el usuario tiene un perfil de cliente
                sucursal_origen=sucursal,
                estado="pendiente",
                total=total
            )
            # Crear el detalle del pedido
            DetallePedido.objects.create(
                pedido=pedido,
                medicamento=medicamento,
                cantidad=cantidad,
                subtotal=total
            )
            # Reducir el stock del medicamento
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

    return render(request, "sales/realizar_venta.html", {"sucursal": sucursal, "medicamentos": medicamentos})


def seguimiento(request):
    """Seguimiento de pedidos (mostrar el estado y progreso)."""
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-fecha')
    return render(request, 'sales/seguimiento.html', {'pedidos': pedidos})


def seleccionar_sucursal(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/seleccionar_sucursal.html', {'sucursales': sucursales})