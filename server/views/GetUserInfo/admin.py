from .models import PlaceholderModel

from django.contrib import admin


@admin.register(PlaceholderModel)
class PlaceholderModelAdmin(admin.ModelAdmin):
    pass