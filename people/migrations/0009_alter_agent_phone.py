# Generated by Django 3.2.18 on 2023-03-06 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20230306_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='phone',
            field=models.CharField(max_length=50),
        ),
    ]