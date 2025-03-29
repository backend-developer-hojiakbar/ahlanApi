from django.db import models
import random
import string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from .managers import CustomUserManager


class Object(models.Model):
    name = models.CharField(max_length=255)
    total_apartments = models.PositiveIntegerField()  # Manfiy bo‘lmasligi uchun
    floors = models.PositiveIntegerField()
    address = models.TextField()
    description = models.TextField(blank=True)  # Majburiy emas
    image = models.ImageField(upload_to='objects/', blank=True, null=True)  # Rasm majburiy emas

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
    room_number = models.PositiveIntegerField()  # Xona raqami
    rooms = models.PositiveIntegerField()  # Xonalar soni
    area = models.FloatField()  # Maydon
    floor = models.PositiveIntegerField()  # Qavat
    price = models.DecimalField(max_digits=12, decimal_places=2)  # Narx uchun katta maydon
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
        if amount < 0:
            raise ValueError("Qo‘shiladigan summa manfiy bo‘lishi mumkin emas!")
        self.balance += amount
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