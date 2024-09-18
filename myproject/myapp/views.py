from django.shortcuts import render, get_object_or_404, redirect
from .models import Player, Pdf  # Asegúrate de que el nombre del modelo es 'Pdf', no 'PDF'
from .forms import PlayerForm, CoverImageForm, PDFForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

from .forms import CustomLoginForm
from django.contrib.auth.views import LogoutView as DjangoLogoutView

class CustomLogoutView(DjangoLogoutView):
    next_page = '/' 

@login_required
def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

@login_required
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})

@login_required
def player_create(request):
    # Formset para PDF
    PDFFormSet = inlineformset_factory(Player, Pdf, form=PDFForm, extra=3, can_delete=True)
    
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, request.FILES)
        formset = PDFFormSet(request.POST, request.FILES)

        if player_form.is_valid() and formset.is_valid():
            # Guardar jugador
            player = player_form.save()

            # Guardar los PDFs
            pdfs = formset.save(commit=False)
            for pdf in pdfs:
                pdf.player = player  # Asignar el jugador a cada PDF
                pdf.save()  # Guardar cada PDF

            # Redirigir al listado de jugadores después de guardar
            return redirect('player_list')
    else:
        player_form = PlayerForm()
        formset = PDFFormSet()

    return render(request, 'player_form.html', {
        'form': player_form,
        'formset': formset,
    })
@login_required
def upload_cover_image(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        form = CoverImageForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_detail', pk=player.pk)
    else:
        form = CoverImageForm(instance=player)
    return render(request, 'upload_cover_image.html', {'form': form, 'player': player})

@login_required
def player_update(request, pk):
    player = Player.objects.get(pk=pk)
    PDFFormSet = inlineformset_factory(Player, Pdf, form=PDFForm, extra=1, can_delete=True)

    if request.method == 'POST':
        player_form = PlayerForm(request.POST, request.FILES, instance=player)
        formset = PDFFormSet(request.POST, request.FILES, instance=player)

        if player_form.is_valid() and formset.is_valid():
            player = player_form.save()
            pdfs = formset.save(commit=False)

            # Guardar o eliminar los PDFs
            for pdf in pdfs:
                pdf.player = player
                pdf.save()

            # Eliminar los PDFs marcados para eliminación
            for pdf_form in formset.deleted_objects:
                pdf_form.delete()

            return redirect('player_list')
    else:
        player_form = PlayerForm(instance=player)
        formset = PDFFormSet(instance=player)

    return render(request, 'player_form.html', {
        'form': player_form,
        'formset': formset,
    })


@login_required
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('player_list')
    return render(request, 'player_confirm_delete.html', {'player': player})

@login_required
def player_search(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(
        nombre__icontains=query
    ) | Player.objects.filter(
        equipo__icontains=query
    ) | Player.objects.filter(
        categoria__icontains=query
    ) | Player.objects.filter(
        posicion__icontains=query
    )
    html = render_to_string('player_search_results.html', {'players': players})
    return JsonResponse(html, safe=False)

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('player_list')  # Redirige a la lista de jugadores después del inicio de sesión
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
