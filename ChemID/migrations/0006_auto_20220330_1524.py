# Generated by Django 3.1.7 on 2022-03-30 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChemID', '0005_auto_20220329_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='spectator',
            name='is_tshirtcombocus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spectator',
            name='is_tshirtcus',
            field=models.BooleanField(default=False),
        ),
    ]
