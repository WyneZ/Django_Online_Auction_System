# Generated by Django 4.2.6 on 2023-10-26 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_reg_login", "0002_alter_item_category_alter_item_highest_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="item_image",
        ),
        migrations.AlterField(
            model_name="item",
            name="highest_price",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name="ImageTable",
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
                ("image_url", models.ImageField(upload_to="images/")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_reg_login.item",
                    ),
                ),
            ],
        ),
    ]
