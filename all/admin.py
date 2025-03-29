from django.contrib import admin
from .models import Object, Apartment, User, ExpenseType, Supplier, Expense


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_apartments', 'floors', 'address')
    search_fields = ('name', 'address')
    list_filter = ('floors', 'total_apartments')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('object', 'room_number', 'rooms', 'floor', 'price', 'status')
    list_filter = ('status', 'object', 'rooms', 'floor')
    search_fields = ('object__name', 'room_number')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fio', 'phone_number', 'user_type', 'balance')
    list_filter = ('user_type', 'balance')
    search_fields = ('fio', 'phone_number', 'kafil_fio')
    fieldsets = (
        (None, {'fields': ('phone_number', 'fio', 'password', 'user_type')}),
        ('Qo‘shimcha', {'fields': ('address', 'object_id', 'apartment_id', 'telegram_chat_id', 'balance')}),
        ('Kafil', {'fields': ('kafil_fio', 'kafil_address', 'kafil_phone_number')}),
    )


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'email', 'balance')
    list_filter = ('balance',)
    search_fields = ('company_name', 'phone_number', 'email')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount', 'date', 'expense_type', 'status')
    list_filter = ('status', 'expense_type', 'object', 'date')
    search_fields = ('supplier__company_name', 'comment')