# Generated by Django 4.2.15 on 2024-09-03 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0013_partita_cliente"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="data",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
