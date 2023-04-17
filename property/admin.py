from django.contrib import admin

from .models import Flat, Complaint, Owner


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ('address', 'price', 'new_building', 'construction_year', 'town', 'owner_pure_phonenumber')
    list_editable = ('new_building',)
    list_filter = ('new_building', 'active', 'town', 'construction_year')
    search_fields = ('town', 'address', 'owner')
    readonly_fields = ('created_at',)
    raw_id_fields = ('liked_by',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'flat')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_pure_phonenumber')
    raw_id_fields = ('flat',)
