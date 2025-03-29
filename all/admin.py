from django.contrib import admin
from .models import Object, Apartment, User


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_apartments', 'floors', 'address')
    search_fields = ('name', 'address')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('object', 'room_number', 'rooms', 'floor', 'price', 'status')
    list_filter = ('status', 'object')
    search_fields = ('object__name', 'room_number')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fio', 'phone_number', 'user_type', 'balance')
    list_filter = ('user_type',)
    search_fields = ('fio', 'phone_number', 'kafil_fio')
    fieldsets = (
        (None, {'fields': ('phone_number', 'fio', 'password', 'user_type')}),
        ('Qo‘shimcha', {'fields': ('address', 'object_id', 'apartment_id', 'telegram_chat_id', 'balance')}),
        ('Kafil', {'fields': ('kafil_fio', 'kafil_address', 'kafil_phone_number')}),
    )