from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('emlak/', views.property_list, name='property_list'),
    path('arsa/', views.property_list, {'type_filter': 'ARSA'}, name='land_list'),
    path('konut/', views.property_list, {'type_filter': 'KONUT'}, name='residential_list'),
    path('isyeri/', views.property_list, {'type_filter': 'ISYERI'}, name='commercial_list'),
    path('tarla/', views.property_list, {'type_filter': 'TARLA'}, name='field_list'),
    path('emlak/<int:pk>/', views.property_detail, name='property_detail'),
    path('iletisim/', views.contact, name='contact'),
] 