# Generated by Django 5.0.3 on 2024-03-14 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("car_rental", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InsurancePolicy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("policy_number", models.CharField(max_length=100)),
                ("provider_name", models.CharField(max_length=100)),
                ("coverage_start_date", models.DateField()),
                ("coverage_end_date", models.DateField()),
                (
                    "premium_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "deductible_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="photos/")),
            ],
        ),
        migrations.CreateModel(
            name="CustomerReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.IntegerField()),
                ("review_text", models.TextField()),
                ("date_posted", models.DateField()),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="car_rental.car"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="car_rental.customuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RentalTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_date", models.DateField()),
                (
                    "transaction_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("payment_method", models.CharField(max_length=100)),
                ("transaction_status", models.CharField(max_length=100)),
                (
                    "rental_reservation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="car_rental.rentalreservation",
                    ),
                ),
            ],
        ),
    ]
