# Generated by Django 5.1.7 on 2025-04-16 06:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Xarajat turi',
                'verbose_name_plural': 'Xarajat turlari',
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('total_apartments', models.PositiveIntegerField()),
                ('floors', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='objects/')),
            ],
            options={
                'verbose_name': 'Obyekt',
                'verbose_name_plural': 'Obyektlar',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('contact_person_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
            options={
                'verbose_name': 'Yetkazib beruvchi',
                'verbose_name_plural': 'Yetkazib beruvchilar',
            },
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=100)),
                ('rooms', models.PositiveIntegerField()),
                ('area', models.FloatField()),
                ('floor', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('bosh', 'Bo‘sh'), ('band', 'Band qilingan'), ('muddatli', 'Muddatli'), ('sotilgan', 'Sotilgan')], default='bosh', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('secret_code', models.CharField(editable=False, max_length=8, unique=True)),
                ('reserved_until', models.DateTimeField(blank=True, null=True)),
                ('reservation_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('total_payments', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='all.object')),
            ],
            options={
                'verbose_name': 'Xonadon',
                'verbose_name_plural': 'Xonadonlar',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('fio', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('sotuvchi', 'Sotuvchi'), ('buxgalter', 'Buxgalter'), ('mijoz', 'Mijoz')], default='mijoz', max_length=20)),
                ('telegram_chat_id', models.CharField(blank=True, max_length=50, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, help_text='Foydalanuvchi balansi (so‘mda)', max_digits=12)),
                ('kafil_fio', models.CharField(blank=True, max_length=255, null=True)),
                ('kafil_address', models.TextField(blank=True, null=True)),
                ('kafil_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('apartment_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owners', to='all.apartment')),
                ('object_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='all.object')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('naqd', 'Naqd pul'), ('muddatli', 'Muddatli to‘lov'), ('ipoteka', 'Ipoteka'), ('subsidiya', 'Subsidiya'), ('band', 'Band qilish'), ('barter', 'Barter')], default='naqd', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('initial_payment', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12)),
                ('interest_rate', models.FloatField(blank=True, default=0.0)),
                ('duration_months', models.PositiveIntegerField(blank=True, default=0)),
                ('monthly_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('due_date', models.PositiveIntegerField(default=1, help_text='Har oy qaysi kunda to‘lov bo‘lishi kerak (1-31)')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('paid', 'To‘langan'), ('overdue', 'Muddati o‘tgan')], default='pending', max_length=20)),
                ('additional_info', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_date', models.DateTimeField(blank=True, help_text='Foydalanuvchi to‘lov sanasini kiritadi', null=True)),
                ('reservation_deadline', models.DateTimeField(blank=True, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='all.apartment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'To‘lov',
                'verbose_name_plural': 'To‘lovlar',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('kvitansiya', 'Kvitansiya'), ('shartnoma', 'Shartnoma'), ('chek', 'Chek'), ('boshqa', 'Boshqa')], default='shartnoma', max_length=20)),
                ('docx_file', models.FileField(blank=True, null=True, upload_to='contracts/docx/')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='contracts/pdf/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='documents/images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='all.payment')),
            ],
            options={
                'verbose_name': 'Hujjat',
                'verbose_name_plural': 'Hujjatlar',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('To‘langan', 'To‘langan'), ('Kutilmoqda', 'Kutilmoqda')], default='Kutilmoqda', max_length=50)),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='all.expensetype')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='all.object')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='all.supplier')),
            ],
            options={
                'verbose_name': 'Xarajat',
                'verbose_name_plural': 'Xarajatlar',
            },
        ),
        migrations.CreateModel(
            name='SupplierPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('payment_type', models.CharField(choices=[('naqd', 'Naqd pul'), ('muddatli', 'Muddatli to‘lov'), ('ipoteka', 'Ipoteka')], default='naqd', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_payments', to='all.supplier')),
            ],
            options={
                'verbose_name': 'Yetkazib beruvchi to‘lovi',
                'verbose_name_plural': 'Yetkazib beruvchi to‘lovlari',
            },
        ),
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('payment_type', models.CharField(choices=[('naqd', 'Naqd pul'), ('muddatli', 'Muddatli to‘lov'), ('ipoteka', 'Ipoteka')], default='naqd', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Foydalanuvchi to‘lovi',
                'verbose_name_plural': 'Foydalanuvchi to‘lovlari',
            },
        ),
    ]
