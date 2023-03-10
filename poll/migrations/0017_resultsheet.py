# Generated by Django 3.2.18 on 2023-03-05 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0016_auto_20230305_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField(blank=True, help_text='Total number of votes', null=True, verbose_name='Total number of votes')),
                ('total_valid_votes', models.IntegerField(blank=True, help_text='Total number of valid votes', null=True, verbose_name='Total number of valid votes')),
                ('total_invalid_votes', models.IntegerField(blank=True, help_text='Total number of invalid votes', null=True, verbose_name='Total number of invalid votes')),
                ('result_sheet', models.FileField(blank=True, default=None, help_text='Result verification sheet', null=True, upload_to='results/%Y/%m/%d')),
                ('station_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Stational Approved At')),
                ('constituency_approved_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Constituency Approved At')),
                ('regional_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Regional Approved At')),
                ('national_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Regional Approved At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35, null=True)),
                ('constituency_agent', models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituency_result_sheets', to=settings.AUTH_USER_MODEL)),
                ('nation_agent', models.ForeignKey(blank=True, default=None, help_text='National agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='national_result_sheets', to=settings.AUTH_USER_MODEL)),
                ('region_agent', models.ForeignKey(blank=True, default=None, help_text='Regional agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_result_sheets', to=settings.AUTH_USER_MODEL)),
                ('station_agent', models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_result_sheets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'poll_result_sheet',
            },
        ),
    ]
