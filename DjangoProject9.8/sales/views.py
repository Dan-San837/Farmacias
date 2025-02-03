from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Sucursal, Pedido, DetallePedido, Medicamento, Cliente
from .forms import VentaMedicamentoForm, TransferenciaMedicamentoForm, PedidoForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def venta_medicamento(request):
    if request.method == "POST":
        form = VentaMedicamentoForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            if venta.medicamento_sucursal.stock >= venta.cantidad:
                venta.usuario = request.user
                venta.medicamento_sucursal.stock -= venta.cantidad
                venta.medicamento_sucursal.save()
                venta.save()
                messages.success(request, "Venta registrada correctamente")
                return redirect('ventas')
            else:
                messages.error(request, "Stock insuficiente")
    else:
        form = VentaMedicamentoForm()
    return render(request, "sales/venta_medicamento.html", {"form": form})

@login_required
def transferencia_medicamento(request):
    if request.method == "POST":
        form = TransferenciaMedicamentoForm(request.POST)
        if form.is_valid():
            transferencia = form.save(commit=False)
            if transferencia.medicamento_sucursal_origen.stock >= transferencia.cantidad:
                transferencia.medicamento_sucursal_origen.stock -= transferencia.cantidad
                transferencia.medicamento_sucursal_origen.save()
                transferencia.estado = "pendiente"
                transferencia.save()
                messages.success(request, "Transferencia registrada")
                return redirect('transferencias')
            else:
                messages.error(request, "Stock insuficiente en la sucursal de origen")
    else:
        form = TransferenciaMedicamentoForm()
    return render(request, "sales/transferencia_medicamento.html", {"form": form})

def index(request):
    """Página principal del módulo de ventas."""
    return render(request, 'sales/index.html')

def ventas_index(request):
    pedidos = Pedido.objects.all()  # Filtra según las reglas de tu sistema
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/index.html', {'pedidos': pedidos, 'sucursales': sucursales})

def ventas_list(request):
    sucursal_id = request.GET.get('sucursal')
    ventas = Pedido.objects.all()
    if sucursal_id and sucursal_id.isdigit():  # Si hay un filtro de sucursal
        ventas = Pedido.objects.filter(sucursal_origen_id=sucursal_id)

    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales para el filtro
    return render(request, 'sales/ventas_list.html', {"ventas": ventas, "sucursales": sucursales})

@login_required
def crear_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)

            # Asignamos el cliente autenticado
            if hasattr(request.user, 'cliente'):
                pedido.cliente = request.user.cliente
            else:
                return render(request, 'sales/crear_pedido.html', {'form': form, 'error': 'No tienes un perfil de cliente'})

            pedido.save()  # Guardamos el pedido para obtener su ID

            # Inicializamos el total del pedido
            total_pedido = 0

            # Guardar los medicamentos seleccionados en DetallePedido
            for medicamento in form.cleaned_data['medicamentos']:
                cantidad = request.POST.get(f'cantidad_{medicamento.id}', 1)  # Capturar la cantidad
                cantidad = int(cantidad) if cantidad.isdigit() else 1

                subtotal = medicamento.precio * cantidad  # Calcular subtotal

                DetallePedido.objects.create(
                    pedido=pedido,
                    medicamento=medicamento,
                    cantidad=cantidad,
                    subtotal=subtotal  # Guardar subtotal en la base de datos
                )

                total_pedido += subtotal  # Sumar al total del pedido

            pedido.total = total_pedido  # Asignar el total calculado
            pedido.save()

            return redirect('sales:seguimiento')

    else:
        form = PedidoForm()

    return render(request, 'sales/crear_pedido.html', {'form': form})

def seguimiento(request):
    """Seguimiento de pedidos (mostrar el estado y progreso)."""
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-fecha')
    return render(request, 'sales/seguimiento.html', {'pedidos': pedidos})

def medicamentos_list(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'sales/medicamentos_list.html', {'medicamentos': medicamentos})

def seleccionar_sucursal(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sales/seleccionar_sucursal.html', {'sucursales': sucursales})

def pedido_detalle(request, pedido_id):
    nombre = Medicamento.objects.get(id=pedido_id)
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.all()
    return render(request, 'sales/pedido_detalle.html', {'pedido': pedido, 'nombre': nombre, 'detalles': detalles})

def actualizar_estado (request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
    return redirect('sales:seguimiento')


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