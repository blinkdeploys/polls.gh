# Generated by Django 3.2.18 on 2023-03-05 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0019_remove_result_result_sheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='result_sheet',
            field=models.ForeignKey(blank=True, default=None, help_text='Result verification sheet', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='poll.resultsheet'),
        ),
    ]
