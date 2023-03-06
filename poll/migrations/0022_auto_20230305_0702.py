# Generated by Django 3.2.18 on 2023-03-05 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0005_auto_20230302_0244'),
        ('poll', '0021_rename_total_votes_result_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultsheet',
            name='position',
            field=models.ForeignKey(blank=True, default=True, help_text='Position', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_sheets', to='poll.position'),
        ),
        migrations.AddField(
            model_name='resultsheet',
            name='station',
            field=models.ForeignKey(blank=True, default=True, help_text='Polling Station', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_sheets', to='geo.station'),
        ),
    ]