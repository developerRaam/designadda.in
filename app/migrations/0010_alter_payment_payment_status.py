# Generated by Django 4.1 on 2023-03-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_payment_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('Failed', 'Failed'), ('Credit', 'Credit'), ('Pending', 'Pending')], default='Pending', max_length=50),
        ),
    ]
