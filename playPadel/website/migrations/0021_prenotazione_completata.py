# Generated by Django 4.2.15 on 2024-12-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_remove_impianto_citta'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenotazione',
            name='completata',
            field=models.BooleanField(default=False),
        ),
    ]
