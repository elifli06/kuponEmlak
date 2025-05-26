from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.managers import InheritanceManager

class Property(models.Model):
    PROPERTY_TYPES = (
        ('ARSA', 'Arsa'),
        ('KONUT', 'Konut'),
        ('ISYERI', 'İşyeri'),
        ('TARLA', 'Tarla'),
        ('DIGER', 'Diğer'),
    )
    
    LISTING_TYPES = (
        ('SATILIK', 'Satılık'),
        ('KIRALIK', 'Kiralık'),
    )

    title = models.CharField(max_length=200, verbose_name='Başlık')
    description = models.TextField(verbose_name='Açıklama')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Fiyat')
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES, verbose_name='Emlak Tipi')
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, verbose_name='İlan Tipi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = InheritanceManager()

    class Meta:
        verbose_name = 'Emlak'
        verbose_name_plural = 'Emlaklar'

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/', verbose_name='Resim')
    is_main = models.BooleanField(default=False, verbose_name='Ana Resim')

    class Meta:
        verbose_name = 'Emlak Resmi'
        verbose_name_plural = 'Emlak Resimleri'

class LandProperty(Property):
    zoning_status = models.CharField(max_length=100, verbose_name='İmar Durumu')
    square_meters = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='m²')
    price_per_square_meter = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='m² Fiyatı')
    block_number = models.CharField(max_length=50, verbose_name='Ada No')
    parcel_number = models.CharField(max_length=50, verbose_name='Parsel No')
    credit_eligibility = models.BooleanField(default=True, verbose_name='Krediye Uygunluk')
    deed_status = models.CharField(max_length=100, verbose_name='Tapu Durumu')
    exchange_possible = models.BooleanField(default=False, verbose_name='Takas')

    class Meta:
        verbose_name = 'Arsa/Tarla'
        verbose_name_plural = 'Arsa/Tarlalar'

class ResidentialProperty(Property):
    gross_square_meters = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Brüt m²')
    net_square_meters = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Net m²')
    room_count = models.PositiveIntegerField(verbose_name='Oda Sayısı')
    floor_count = models.PositiveIntegerField(verbose_name='Kat Sayısı')
    floor_location = models.PositiveIntegerField(verbose_name='Bulunduğu Kat')
    heating_system = models.CharField(max_length=100, verbose_name='Isıtma Sistemi')
    bathroom_count = models.PositiveIntegerField(verbose_name='Banyo Sayısı')
    kitchen_type = models.CharField(max_length=100, verbose_name='Mutfak Tipi')
    has_balcony = models.BooleanField(default=False, verbose_name='Balkon')
    balcony_count = models.PositiveIntegerField(default=0, verbose_name='Balkon Sayısı')
    has_parking = models.BooleanField(default=False, verbose_name='Otopark')
    parking_type = models.CharField(max_length=50, choices=[('ACIK', 'Açık'), ('KAPALI', 'Kapalı')], null=True, blank=True, verbose_name='Otopark Tipi')

    class Meta:
        verbose_name = 'Konut'
        verbose_name_plural = 'Konutlar'

class CommercialProperty(Property):
    square_meters = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='m²')
    heating_status = models.CharField(max_length=100, verbose_name='Isıtma Durumu')
    floor_count = models.PositiveIntegerField(verbose_name='Kat Sayısı')
    floor_location = models.PositiveIntegerField(verbose_name='Bulunduğu Kat')

    class Meta:
        verbose_name = 'İşyeri'
        verbose_name_plural = 'İşyerleri'
