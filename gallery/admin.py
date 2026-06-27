from django.contrib import admin

from .models import Evento, Fotografia


class FotografiaInline(admin.TabularInline):
    model = Fotografia
    extra = 0


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "creado",
    )

    prepopulated_fields = {
        "slug": ("nombre",)
    }

    inlines = [
        FotografiaInline,
    ]


@admin.register(Fotografia)
class FotografiaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "evento",
        "subida",
    )
