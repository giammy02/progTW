# Generated by Django 4.2.15 on 2024-08-30 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0011_alter_users_is_cliente"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="eta",
            field=models.IntegerField(default=18),
            preserve_default=False,
        ),
    ]