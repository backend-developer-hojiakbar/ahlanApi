from django.db import models
import random
import string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from .managers import CustomUserManager
from decimal import Decimal


class Object(models.Model):
    name = models.CharField(max_length=255)
    total_apartments = models.PositiveIntegerField()
    floors = models.PositiveIntegerField()
    address = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='objects/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Obyekt"
        verbose_name_plural = "Obyektlar"


class Apartment(models.Model):
    STATUS_CHOICES = (
        ('bosh', 'Bo‘sh'),
        ('band', 'Band qilingan'),
        ('sotilgan', 'Sotilgan'),
    )

    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='apartments')
    room_number = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    area = models.FloatField()
    floor = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bosh')
    description = models.TextField(blank=True)
    secret_code = models.CharField(max_length=8, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.secret_code:
            self.secret_code = ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.object.name} - {self.rooms} xonali"

    class Meta:
        verbose_name = "Xonadon"
        verbose_name_plural = "Xonadonlar"


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    fio = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    object_id = models.ForeignKey(Object, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    apartment_id = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='owners')
    password = models.CharField(max_length=128)

    USER_TYPES = (
        ('admin', 'Admin'),
        ('sotuvchi', 'Sotuvchi'),
        ('buxgalter', 'Buxgalter'),
        ('mijoz', 'Mijoz'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='mijoz')

    telegram_chat_id = models.CharField(max_length=50, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                  help_text="Foydalanuvchi balansi (so‘mda)")

    kafil_fio = models.CharField(max_length=255, null=True, blank=True)
    kafil_address = models.TextField(null=True, blank=True)
    kafil_phone_number = models.CharField(max_length=15, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['fio']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def add_balance(self, amount):
        if amount < 0 and self.balance + amount < 0 and self.balance == 0:
            self.balance += amount  # Agar balans 0 bo‘lsa, minusga tushishga ruxsat beramiz
        elif amount >= 0 or (amount < 0 and self.balance + amount >= 0):
            self.balance += amount
        else:
            raise ValueError("Balans yetarli emas yoki minusga tushish mumkin emas!")
        self.save()

    def deduct_balance(self, amount):
        if amount < 0:
            raise ValueError("Ayiriladigan summa manfiy bo‘lishi mumkin emas!")
        if self.balance < amount:
            raise ValueError("Balansda yetarli mablag‘ yo‘q!")
        self.balance -= amount
        self.save()

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class ExpenseType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Xarajat turi"
        verbose_name_plural = "Xarajat turlari"


class Supplier(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    description = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Yetkazib beruvchi"
        verbose_name_plural = "Yetkazib beruvchilar"


class Expense(models.Model):
    STATUS_CHOICES = (
        ('To‘langan', 'To‘langan'),
        ('Kutilmoqda', 'Kutilmoqda'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='expenses')
    comment = models.TextField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, related_name='expenses')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='expenses')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Kutilmoqda')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.supplier.balance += self.amount
            self.supplier.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.supplier.company_name} - {self.amount}"

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"


class Payment(models.Model):
    PAYMENT_TYPES = (
        ('naqd', 'Naqd pul'),
        ('muddatli', 'Muddatli to‘lov'),
        ('ipoteka', 'Ipoteka'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='naqd')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)  # Umumiy narx
    initial_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True)  # Boshlang‘ich to‘lov
    interest_rate = models.FloatField(default=0.0, blank=True)  # Foiz (yillik)
    duration_months = models.PositiveIntegerField(default=0, blank=True)  # Muddat (oylarda)
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Har oylik to‘lov
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_monthly_payment(self):
        if self.payment_type == 'muddatli' and self.duration_months > 0:
            remaining_amount = self.total_amount - self.initial_payment
            interest = remaining_amount * (Decimal(str(self.interest_rate)) / Decimal('100'))
            total_with_interest = remaining_amount + interest
            self.monthly_payment = total_with_interest / Decimal(str(self.duration_months))
        elif self.payment_type == 'naqd':
            self.monthly_payment = Decimal('0')
        else:  # Ipoteka uchun soddalashtirilgan hisob
            self.monthly_payment = (self.total_amount - self.initial_payment) / Decimal(str(self.duration_months))

    def save(self, *args, **kwargs):
        self.total_amount = self.apartment.price
        self.calculate_monthly_payment()
        super().save(*args, **kwargs)
        if self.payment_type == 'muddatli' and self.duration_months > 0:
            remaining_amount = self.total_amount - self.initial_payment
            interest = remaining_amount * (Decimal(str(self.interest_rate)) / Decimal('100'))
            total_with_interest = remaining_amount + interest
            self.user.add_balance(-total_with_interest)  # Qarzni minusda qo‘shish

    def __str__(self):
        return f"{self.user.fio} - {self.apartment} - {self.payment_type}"

    class Meta:
        verbose_name = "To‘lov"
        verbose_name_plural = "To‘lovlar"