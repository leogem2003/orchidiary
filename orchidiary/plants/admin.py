from django.contrib import admin

# Register your models here.

from .models import OrchidGenre, OrchidInstance, OrchidVariety

class GenreAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields':('genre', 'description')}),
        ('Coltural requirements', {'fields':(('winter_range', 'summer_range'), 'light', 'humidity', 'ground')}),
        ('Photo', {'fields':('image',)}),
    )

class VarietyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields':(('genre', 'name'), 'is_bothanic', 'hybrid_ancestors')}),
        (('Coltural requirements', {'fields':(('winter_range', 'summer_range'), 'light', 'humidity', 'ground')})),
        (None, {'fields':('image',)}),
    )

class InstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields':('variety',)}),
        ('Pot', {'fields':(('pot_type', 'pot_size'), 'medium')}),
        (None, {'fields':('image',)}),
    )

admin.site.register(OrchidGenre, GenreAdmin)
admin.site.register(OrchidVariety, VarietyAdmin)
admin.site.register(OrchidInstance, InstanceAdmin)
