# Generated by Django 4.2.15 on 2024-11-23 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0019_impianto_citta_alter_partita_giocatori_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="impianto",
            name="citta",
        ),
    ]
