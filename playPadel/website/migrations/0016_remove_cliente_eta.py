# Generated by Django 4.2.15 on 2024-09-05 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0015_campo_numero"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="eta",
        ),
    ]