from django.shortcuts import render, get_object_or_404, redirect
from .forms import MedicamentoForm
from .models import Sucursal, Medicamento, Inventario


def inventario_list(request):
    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales
    sucursal_id = request.GET.get('sucursal')  # Obtener la sucursal seleccionada

    # Filtrar medicamentos por sucursal si se ha seleccionado una
    if sucursal_id:
        medicamentos = Medicamento.objects.filter(sucursal_id=sucursal_id)
    else:
        medicamentos = Medicamento.objects.all()

    return render(request, 'inventory/inventario_list.html', {
        'medicamentos': medicamentos,
        'sucursales': sucursales,
        'sucursal_id': sucursal_id,  # Para mantener el filtro seleccionado
    })

def inventario_detail(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    inventarios = Inventario.objects.filter(sucursal=sucursal)
    return render(request, 'inventory/inventario_detail.html', {'sucursal': sucursal, 'inventarios': inventarios})

def add_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventario_list')  # Redirige a la lista de inventarios
    else:
        form = MedicamentoForm()
    return render(request, 'inventory/add_medicamento.html', {'form': form})

def update_medicamento(request, pk):
    # Recupera el medicamento o lanza un 404 si no existe
    medicamento = get_object_or_404(Medicamento, pk=pk)

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()  # Guarda los cambios en el medicamento
            return redirect('inventory:inventario_list')  # Redirige al listado de medicamentos
    else:
        form = MedicamentoForm(instance=medicamento)  # Prellena el formulario con los datos del medicamento

    # Renderiza el formulario para editar
    return render(request, 'inventory/update_medicamento.html', {'form': form, 'medicamento': medicamento})



