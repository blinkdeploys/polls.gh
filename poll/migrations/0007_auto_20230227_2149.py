# Generated by Django 3.2.18 on 2023-02-27 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0004_alter_station_code'),
        ('poll', '0006_auto_20230226_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='zone_id',
            field=models.ForeignKey(blank=True, help_text='Geographic zone being contested', null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.constituency'),
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together={('office', 'zone_id')},
        ),
        migrations.RemoveField(
            model_name='position',
            name='zone',
        ),
    ]
