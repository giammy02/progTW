# Generated by Django 4.2.15 on 2024-11-23 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0018_alter_impianto_foto_alter_users_foto"),
    ]

    operations = [
        migrations.AddField(
            model_name="impianto",
            name="citta",
            field=models.CharField(default="citta", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="partita",
            name="giocatori",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="partita",
            name="risultato",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]