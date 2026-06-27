from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.inicio,
        name="inicio",
    ),

    path(
        "evento/<slug:slug>/",
        views.detalle_evento,
        name="detalle_evento",
    ),

    path(
        "panel/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "panel/evento/nuevo/",
        views.nuevo_evento,
        name="nuevo_evento",
    ),

    path(
        "panel/evento/<int:pk>/",
        views.editar_evento,
        name="editar_evento",
    ),

    path(
        "panel/evento/<int:pk>/fotos/",
        views.evento_fotos,
        name="evento_fotos",
    ),

    path(
        "panel/evento/<int:pk>/eliminar/",
        views.eliminar_evento,
        name="eliminar_evento",
    ),

    path(
        "panel/foto/<int:pk>/eliminar/",
        views.eliminar_foto,
        name="eliminar_foto",
    ),

    path(
        "panel/evento/<int:pk>/fotos/eliminar/",
        views.eliminar_fotos,
        name="eliminar_fotos",
    ),

]