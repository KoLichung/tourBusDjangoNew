# Generated by Django 3.2.12 on 2022-05-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourBusCore', '0018_user_ispassed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isOwner',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='isPassed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
