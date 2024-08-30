# Generated by Django 4.2.15 on 2024-08-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0008_alter_impianto_foto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="foto",
            field=models.ImageField(
                default="default_profile_pic.png", upload_to="profile_pics"
            ),
        ),
        migrations.AlterField(
            model_name="gestore",
            name="foto",
            field=models.ImageField(
                default="default_profile_pic.png", upload_to="profile_pics"
            ),
        ),
        migrations.AlterField(
            model_name="impianto",
            name="foto",
            field=models.ImageField(
                default="default_impianto_photo.jpg", upload_to="media"
            ),
        ),
    ]