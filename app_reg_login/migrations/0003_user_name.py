# Generated by Django 5.0 on 2024-02-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reg_login', '0002_remove_user_name_alter_item_country_of_origin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
