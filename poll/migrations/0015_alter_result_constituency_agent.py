# Generated by Django 3.2.18 on 2023-03-03 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0014_auto_20230302_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='constituency_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL),
        ),
    ]