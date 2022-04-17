# Generated by Django 3.2.12 on 2022-04-16 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourBusCore', '0008_payinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='depositMoney',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='orderMoney',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='tourbus',
            name='vehicalYearOfManufacture',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]