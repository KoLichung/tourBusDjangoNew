# Generated by Django 3.2.12 on 2022-06-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourBusCore', '0021_order_atmfivedigit'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]