# Generated by Django 5.0.3 on 2024-03-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("car_rental", "0007_remove_customuser_gender_customuser_birth_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="fname",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="lname",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="usern",
        ),
        migrations.AddField(
            model_name="customuser",
            name="fullname",
            field=models.CharField(default="", max_length=100),
        ),
    ]
