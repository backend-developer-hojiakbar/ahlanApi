# Generated by Django 5.1.7 on 2025-04-12 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0003_alter_apartment_status_alter_payment_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='payment',
            name='bank_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
