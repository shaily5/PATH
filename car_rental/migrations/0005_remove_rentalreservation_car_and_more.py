# Generated by Django 5.0.3 on 2024-03-16 15:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("car_rental", "0004_remove_rentalreservation_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rentalreservation",
            name="car",
        ),
        migrations.RemoveField(
            model_name="rentalreservation",
            name="dropoff_location",
        ),
        migrations.RemoveField(
            model_name="rentalreservation",
            name="total_cost",
        ),
    ]
