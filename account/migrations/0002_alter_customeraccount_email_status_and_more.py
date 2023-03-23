# Generated by Django 4.1 on 2023-03-21 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraccount',
            name='email_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Deactive', 'Deactive')], default='Deactive', max_length=10),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Deactive', 'Deactive')], default='Active', max_length=10),
        ),
    ]
