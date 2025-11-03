from django.shortcuts import render
from django.db.models import Q
from .models import Property, LandProperty, ResidentialProperty, CommercialProperty
from django.http import Http404
import unicodedata

def normalize_text(text):
    # Türkçe karakterleri normalize et
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if not unicodedata.combining(c))

def home(request):
    properties = Property.objects.all().order_by('-created_at')[:25]
    return render(request, 'properties/home.html', {
        'properties': properties
    })

def property_list(request, type_filter=None):
    property_type = request.GET.get('type', type_filter)
    listing_type = request.GET.get('listing_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('q', '')

    # Ana sorguyu oluştur
    if property_type == 'ARSA':
        properties = LandProperty.objects.all()
    elif property_type == 'KONUT':
        properties = ResidentialProperty.objects.all()
    elif property_type == 'ISYERI':
        properties = CommercialProperty.objects.all()
    elif property_type == 'TARLA':
        properties = LandProperty.objects.filter(property_type='TARLA')
    else:
        properties = Property.objects.select_subclasses()

    # Filtreleri uygula
    if listing_type:
        properties = properties.filter(listing_type=listing_type)

    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Arama sorgusunu işle
    if search_query:
        # Sorguyu normalize et
        normalized_query = normalize_text(search_query)
        query_parts = normalized_query.split()
        
        # Her kelime için arama filtresi oluştur
        title_filter = Q()
        content_filter = Q()
        
        for part in query_parts:
            if part:
                # Başlıkta arama
                title_filter |= Q(title__icontains=part)
                
                # İçerikte arama
                content_filter |= Q(description__icontains=part)
                
                # Türkçe karakter dönüşümleri
                tr_alternatives = {
                    'i': 'ı', 'ı': 'i',
                    'o': 'ö', 'ö': 'o',
                    'u': 'ü', 'ü': 'u',
                    's': 'ş', 'ş': 's',
                    'g': 'ğ', 'ğ': 'g',
                    'c': 'ç', 'ç': 'c'
                }
                
                # Alternatif karakterlerle arama
                for old, new in tr_alternatives.items():
                    if old in part:
                        alt_query = part.replace(old, new)
                        title_filter |= Q(title__icontains=alt_query)
                        content_filter |= Q(description__icontains=alt_query)

        # Başlık ve içerik aramalarını birleştir
        properties = properties.filter(title_filter | content_filter).distinct()
        
        # Başlıkta geçenleri üste çıkar
        properties = properties.extra(
            select={'title_match': "CASE WHEN LOWER(title) LIKE %s THEN 1 ELSE 0 END"},
            select_params=['%' + normalized_query.lower() + '%'],
            order_by=['-title_match', '-created_at']
        )

    else:
        properties = properties.order_by('-created_at')

    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'property_type': property_type,
        'listing_type': listing_type,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query
    })

def property_detail(request, pk):
    try:
        property = Property.objects.select_subclasses().get(pk=pk)
    except Property.DoesNotExist:
        raise Http404("Emlak bulunamadı")

    return render(request, 'properties/property_detail.html', {
        'property': property
    })

def contact(request):
    return render(request, 'properties/contact.html', {
        'email': 'kuponemlaknigde@gmail.com',
        'phone': '0538 402 32 80',
        'agent_name': 'Zekiye GÖKTÜRK'
    })
