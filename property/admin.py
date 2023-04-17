from django.contrib import admin

from .models import Flat, Complaint, Owner


class FlatOwnerInstance(admin.TabularInline):
    model = Owner.flats.through
    raw_id_fields = ['owner']


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    fields = (
        'active',
        ('price', 'town', 'town_district'),
        ('description', 'construction_year'),
        ('address', 'new_building'),
        ('floor', 'rooms_number', 'living_area', 'has_balcony'),
    )
    list_display = ('address', 'price', 'new_building', 'construction_year', 'town', 'display_owners_phonenumber')
    list_editable = ('new_building',)
    list_filter = ('new_building', 'active', 'has_balcony')
    search_fields = ('town', 'address', 'construction_year')
    readonly_fields = ('created_at',)
    raw_id_fields = ('liked_by',)
    inlines = (FlatOwnerInstance, )


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'flat')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_pure_phonenumber')
    raw_id_fields = ('flats',)
