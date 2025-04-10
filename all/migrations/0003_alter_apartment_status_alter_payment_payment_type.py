# Generated by Django 5.1.7 on 2025-04-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0002_remove_supplier_email_apartment_reservation_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='status',
            field=models.CharField(choices=[('bosh', 'Bo‘sh'), ('band', 'Band qilingan'), ('muddatli', 'Muddatli'), ('sotilgan', 'Sotilgan')], default='bosh', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('naqd', 'Naqd pul'), ('muddatli', 'Muddatli to‘lov'), ('ipoteka', 'Ipoteka'), ('subsidiya', 'Subsidiya'), ('band', 'Band qilish'), ('barter', 'Barter')], default='naqd', max_length=20),
        ),
    ]
