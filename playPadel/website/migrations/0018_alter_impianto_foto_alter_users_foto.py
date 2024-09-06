# Generated by Django 4.2.15 on 2024-09-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0017_remove_gestore_user_alter_users_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="impianto",
            name="foto",
            field=models.ImageField(
                blank=True,
                default="media/default_impianto_photo.jpg",
                upload_to="media",
            ),
        ),
        migrations.AlterField(
            model_name="users",
            name="foto",
            field=models.ImageField(
                blank=True,
                default="profile_pics/default_profile_pic.png",
                upload_to="profile_pics",
            ),
        ),
    ]
