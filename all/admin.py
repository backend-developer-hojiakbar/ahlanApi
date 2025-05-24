from django.contrib import admin
from django.utils import timezone
from .models import Object, Apartment, User, ExpenseType, Supplier, Expense, Payment, Document, UserPayment, \
    SupplierPayment


# Agar User modelingiz AbstractUser'dan meros olgan bo'lsa, AuthUserAdmin'dan foydalanish yaxshiroq:
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from django.utils.translation import gettext_lazy as _ # Tarjimalar uchun

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_apartments', 'floors', 'address')
    search_fields = ('name', 'address')
    list_filter = ('floors', 'total_apartments')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
    'object', 'room_number', 'rooms', 'floor', 'price', 'status', 'reserved_until', 'total_payments', 'balance',
    'total_overdue')
    list_filter = ('status', 'object', 'rooms', 'floor')
    search_fields = ('object__name', 'room_number')
    actions = ['add_balance', 'check_overdue_payments']

    def total_overdue(self, obj):
        return obj.get_overdue_payments()['total_overdue']

    total_overdue.short_description = "Muddati o‘tgan summa"

    def add_balance(self, request, queryset):
        for apartment in queryset:
            apartment.add_balance(1000000)
        self.message_user(request, "Tanlangan xonadonlarga balans qo‘shildi!")

    def check_overdue_payments(self, request, queryset):
        for apartment in queryset:
            overdue_data = apartment.get_overdue_payments()
            if overdue_data['overdue_payments']:
                self.message_user(
                    request,
                    f"{apartment} uchun {len(overdue_data['overdue_payments'])} ta muddati o‘tgan to‘lov topildi, jami: {overdue_data['total_overdue']} so‘m!"
                )
        self.message_user(request, "Muddati o‘tgan to‘lovlar tekshirildi!")


@admin.register(User)
class UserAdmin(
    admin.ModelAdmin):  # Agar User modeli AbstractUser'dan vorislik qilsa, bu yerda AuthUserAdmin dan vorislik oling
    list_display = (
        'username',  # Agar User modelingizda username bo'lsa
        'fio',
        'email',  # Agar User modelingizda email bo'lsa
        'phone_number',
        'user_type',
        'is_staff',
        'is_active',
        'is_superuser',
        'balance',
        'last_login',
        'date_joined'
    )
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')  # groups ni ham qo'shdim
    search_fields = (
        'username',  # Agar User modelingizda username bo'lsa
        'fio',
        'email',  # Agar User modelingizda email bo'lsa
        'phone_number',
        'kafil_fio'
    )

    # Agar admin.ModelAdmin'dan foydalanayotgan bo'lsangiz va parolni to'g'ri o'zgartirish kerak bo'lsa,
    # Django'ning UserChangeForm va UserCreationForm'laridan foydalanish yoki save_model metodini override qilish kerak bo'ladi.
    # Eng yaxshi yechim UserAdmin'ni AuthUserAdmin'dan meros olishdir.
    # form = UserChangeForm # Agar User modeli AbstractUser bilan mos bo'lsa
    # add_form = UserCreationForm # Agar User modeli AbstractUser bilan mos bo'lsa

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': (
                'username',  # Agar User modelingizda username bo'lsa
                'password',
                # DIQQAT: Bu yerda parol xesh ko'rinishida bo'ladi. Parolni o'zgartirish uchun AuthUserAdmin yaxshiroq.
                'fio',
                'email',  # Agar User modelingizda email bo'lsa
                'phone_number',
                'user_type'
            )
        }),
        ('Qo‘shimcha ma‘lumotlar', {
            'fields': ('address', 'object_id', 'apartment_id', 'telegram_chat_id', 'balance')
        }),
        ('Kafil ma‘lumotlari', {
            'fields': ('kafil_fio', 'kafil_address', 'kafil_phone_number')
        }),
        ('Huquqlar', {  # Permissions
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Muhim sanalar', {  # Important dates
            'fields': ('last_login', 'date_joined')
        }),
    )
    # Faqat o'qish uchun mo'ljallangan maydonlar
    readonly_fields = ('last_login', 'date_joined')

    # Agar User modelingiz AbstractUser'dan meros olmasa va parolni admin panel orqali
    # o'rnatmoqchi/o'zgartirmoqchi bo'lsangiz, save_model ni override qilishingiz kerak bo'ladi.
    # Masalan:
    # def save_model(self, request, obj, form, change):
    #     if 'password' in form.changed_data:
    #         if form.cleaned_data['password']: # Agar parol kiritilgan bo'lsa
    #             obj.set_password(form.cleaned_data['password'])
    #         elif not obj.pk: # Agar yangi obyekt va parol bo'sh bo'lsa (bu holat kam uchraydi)
    #             obj.set_unusable_password()
    #     super().save_model(request, obj, form, change)


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
    list_display = (
        'user', 'apartment', 'payment_type', 'total_amount', 'initial_payment',
        'monthly_payment', 'due_date', 'paid_amount', 'status', 'created_at',
        'payment_date', 'reservation_deadline', 'bank_name', 'total_overdue'
    )
    list_filter = ('payment_type', 'status', 'created_at', 'payment_date')
    search_fields = ('user__fio', 'apartment__room_number')
    actions = ['process_payment', 'check_overdue_payments']
    readonly_fields = ('total_overdue',)  # get_overdue_payments natijasini ko'rsatish uchun

    def total_overdue(self, obj):
        overdue_data = obj.get_overdue_payments()
        return overdue_data.get('total_overdue', 0) if isinstance(overdue_data, dict) else 0

    total_overdue.short_description = "Muddati o‘tgan summa"

    def process_payment(self, request, queryset):
        for payment in queryset:
            payment.process_payment(amount=1000000)  # Bu yerda miqdorni dinamik qilish kerak bo'lishi mumkin
        self.message_user(request, "Tanlangan to‘lovlar qayta ishlandi!")

    def check_overdue_payments(self, request, queryset):
        for payment in queryset:
            payment.update_status()  # Avval statusni yangilaymiz
            overdue_data = payment.get_overdue_payments()
            if overdue_data.get('overdue_payments'):
                self.message_user(
                    request,
                    f"{payment.user.fio if payment.user else 'Noma\'lum foydalanuvchi'} uchun {len(overdue_data['overdue_payments'])} ta muddati o‘tgan to‘lov topildi, jami: {overdue_data['total_overdue']} so‘m!"
                )
        self.message_user(request, "Muddati o‘tgan to‘lovlar tekshirildi!")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Barcha 'pending' statusidagi to'lovlar uchun statusni yangilash
        # Bu har bir sahifa yuklanishida ishlaydi, ehtiyot bo'ling, katta ma'lumotlar bazasida sekinlashishi mumkin
        # Yaxshiroq yechim - buni faqat kerak bo'lganda (masalan, action orqali) chaqirish yoki cron job orqali
        # for payment in qs.filter(status='pending'):
        #     payment.update_status()
        return qs

    def changelist_view(self, request, extra_context=None):
        today = timezone.now().date()  # Faqat sanani olamiz
        # `due_date` maydoni DateTimeField bo'lsa, `__date` dan foydalanish kerak
        # Agar DateField bo'lsa, to'g'ridan-to'g'ri solishtirish mumkin
        due_payments = Payment.objects.filter(due_date__date=today,
                                              status='pending')  # due_date modelda qanday ekanligiga qarab o'zgartiring

        if due_payments.exists():
            extra_context = extra_context or {}
            extra_context[
                'payment_reminder'] = f"Bugun ({today.strftime('%d-%m-%Y')}) {due_payments.count()} ta to‘lov muddati yetdi!"
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