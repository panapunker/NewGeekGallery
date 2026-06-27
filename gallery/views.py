from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Evento
from django.db import transaction
from .models import Evento, Fotografia


# ===========================
# PARTE PÚBLICA
# ===========================

def inicio(request):

    eventos = Evento.objects.all()

    return render(
        request,
        "gallery/inicio.html",
        {
            "eventos": eventos,
        },
    )


def detalle_evento(request, slug):

    evento = get_object_or_404(
        Evento,
        slug=slug,
    )

    return render(
        request,
        "gallery/detalle_evento.html",
        {
            "evento": evento,
        },
    )


# ===========================
# PANEL PRIVADO
# ===========================

@staff_member_required
def dashboard(request):

    eventos = Evento.objects.all()

    return render(
        request,
        "panel/dashboard.html",
        {
            "eventos": eventos,
        },
    )


# ===========================
# CREAR EVENTO
# ===========================

@staff_member_required
def nuevo_evento(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        portada = request.FILES.get("portada")
        fotografias = request.FILES.getlist("fotografias")

        if not nombre:
            messages.error(request, "Debes escribir el nombre del evento.")
            return redirect("nuevo_evento")

        if not portada:
            messages.error(request, "Debes seleccionar una portada.")
            return redirect("nuevo_evento")

        with transaction.atomic():

            evento = Evento.objects.create(
                nombre=nombre,
                portada=portada,
            )

            for foto in fotografias:

                Fotografia.objects.create(
                    evento=evento,
                    imagen=foto,
                )

        messages.success(request, "Evento creado correctamente.")

        return redirect("dashboard")

    return render(
        request,
        "panel/evento_form.html",
    )


# ===========================
# EDITAR EVENTO
# ===========================

@staff_member_required
def editar_evento(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk,
    )

    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()

        portada = request.FILES.get("portada")

        if nombre:

            evento.nombre = nombre

        if portada:

            evento.portada = portada

        evento.save()

        messages.success(
            request,
            "Evento actualizado correctamente.",
        )

        return redirect(
            "dashboard",
        )

    return render(
        request,
        "panel/evento_editar.html",
        {
            "evento": evento,
        },
    )


# ===========================
# ELIMINAR EVENTO
# ===========================

@staff_member_required
def eliminar_evento(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk,
    )

    if request.method == "POST":

        evento.delete()

        messages.success(
            request,
            "Evento eliminado correctamente.",
        )

        return redirect(
            "dashboard",
        )

    return render(
        request,
        "panel/evento_eliminar.html",
        {
            "evento": evento,
        },
    )
# ==========================================
# ADMINISTRAR FOTOGRAFÍAS
# ==========================================

@staff_member_required
def evento_fotos(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk,
    )

    if request.method == "POST":

        with transaction.atomic():

            archivos = request.FILES.getlist("fotografias")

            for archivo in archivos:

                Fotografia.objects.create(
                    evento=evento,
                    imagen=archivo,
                )

        messages.success(
            request,
            "Fotografías agregadas correctamente.",
        )

        return redirect(
            "evento_fotos",
            pk=evento.id,
        )

    return render(
        request,
        "panel/evento_fotos.html",
        {
            "evento": evento,
        },
    )


# ==========================================
# ELIMINAR UNA FOTOGRAFÍA
# ==========================================

@staff_member_required
def eliminar_foto(request, pk):

    fotografia = get_object_or_404(
        Fotografia,
        pk=pk,
    )

    evento = fotografia.evento

    fotografia.delete()

    messages.success(
        request,
        "Fotografía eliminada.",
    )

    return redirect(
        "evento_fotos",
        pk=evento.id,
    )


# ==========================================
# ELIMINAR VARIAS FOTOGRAFÍAS
# ==========================================

@staff_member_required
def eliminar_fotos(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk,
    )

    if request.method == "POST":

        ids = request.POST.getlist("fotos")

        Fotografia.objects.filter(
            id__in=ids,
            evento=evento,
        ).delete()

        messages.success(
            request,
            "Fotografías eliminadas.",
        )

    return redirect(
        "evento_fotos",
        pk=evento.id,
    )
