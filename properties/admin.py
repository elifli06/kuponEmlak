from django.contrib import admin
from .models import Property, PropertyImage, LandProperty, ResidentialProperty, CommercialProperty

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    min_num = 1
    max_num = 10

@admin.register(LandProperty)
class LandPropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price', 'listing_type', 'square_meters', 'zoning_status', 'created_at')
    list_filter = ('listing_type', 'credit_eligibility', 'exchange_possible')
    search_fields = ('title', 'description', 'block_number', 'parcel_number')

@admin.register(ResidentialProperty)
class ResidentialPropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price', 'listing_type', 'room_count', 'gross_square_meters', 'created_at')
    list_filter = ('listing_type', 'has_parking', 'has_balcony')
    search_fields = ('title', 'description')

@admin.register(CommercialProperty)
class CommercialPropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price', 'listing_type', 'square_meters', 'floor_count', 'created_at')
    list_filter = ('listing_type',)
    search_fields = ('title', 'description')
