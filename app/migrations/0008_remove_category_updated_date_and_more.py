# Generated by Django 4.1 on 2023-03-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product_mrp_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='updated_date',
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Credit', 'Credit')], default='Pending', max_length=50),
        ),
    ]
