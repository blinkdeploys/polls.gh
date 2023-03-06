# Generated by Django 3.2.18 on 2023-03-06 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('people', '0007_auto_20230302_0244'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='zone_ct',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'geo'), ('model', 'Nation')), models.Q(('app_label', 'geo'), ('model', 'Region')), models.Q(('app_label', 'geo'), ('model', 'Constituency')), models.Q(('app_label', 'geo'), ('model', 'Station')), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorized_zone', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='agent',
            name='zone_id',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
    ]
