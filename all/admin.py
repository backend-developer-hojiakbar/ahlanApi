from django.contrib import admin
from django.utils import timezone
from .models import Object, Apartment, User, ExpenseType, Supplier, Expense, Payment, Document, UserPayment, SupplierPayment

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_apartments', 'floors', 'address')
    search_fields = ('name', 'address')
    list_filter = ('floors', 'total_apartments')

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('object', 'room_number', 'rooms', 'floor', 'price', 'status', 'reserved_until', 'total_payments', 'balance')
    list_filter = ('status', 'object', 'rooms', 'floor')
    search_fields = ('object__name', 'room_number')
    actions = ['add_balance']

    def add_balance(self, request, queryset):
        for apartment in queryset:
            apartment.add_balance(1000000)  # Masalan, 1 million so‘m qo‘shish
        self.message_user(request, "Tanlangan xonadonlarga balans qo‘shildi!")

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
    list_display = ('company_name', 'phone_number', 'balance')
    list_filter = ('balance',)
    search_fields = ('company_name', 'phone_number')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount', 'date', 'expense_type', 'status')
    list_filter = ('status', 'expense_type', 'object', 'date')
    search_fields = ('supplier__company_name', 'comment')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartment', 'payment_type', 'total_amount', 'initial_payment', 'monthly_payment', 'due_date', 'paid_amount', 'status', 'created_at', 'reservation_deadline', 'bank_name')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('user__fio', 'apartment__room_number')
    actions = ['process_payment']

    def process_payment(self, request, queryset):
        for payment in queryset:
            payment.process_payment(amount=1000000)  # Masalan, 1 million so‘m qo‘shish
        self.message_user(request, "Tanlangan to‘lovlar qayta ishlandi!")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today = timezone.now().day
        overdue = qs.filter(due_date__lt=today, status='pending')
        for payment in overdue:
            payment.update_status()
        return qs

    def changelist_view(self, request, extra_context=None):
        today = timezone.now().day
        due_payments = Payment.objects.filter(due_date=today, status='pending')
        if due_payments.exists():
            extra_context = extra_context or {}
            extra_context['payment_reminder'] = f"Bugun ({today}-kun) {due_payments.count()} ta to‘lov muddati yetdi!"
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'document_type', 'created_at')
    list_filter = ('document_type', 'created_at')
    search_fields = ('payment__user__fio',)

@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_type', 'date', 'description')
    list_filter = ('payment_type', 'date')
    search_fields = ('user__fio', 'description')

@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'amount', 'payment_type', 'date', 'description')
    list_filter = ('payment_type', 'date')
    search_fields = ('supplier__company_name', 'description')