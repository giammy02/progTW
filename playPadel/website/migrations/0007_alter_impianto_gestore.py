# Generated by Django 4.2.15 on 2024-08-12 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_alter_impianto_gestore"),
    ]

    operations = [
        migrations.AlterField(
            model_name="impianto",
            name="gestore",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="website.gestore"
            ),
        ),
    ]