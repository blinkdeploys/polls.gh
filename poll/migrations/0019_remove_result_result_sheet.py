# Generated by Django 3.2.18 on 2023-03-05 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0018_auto_20230305_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='result_sheet',
        ),
    ]
