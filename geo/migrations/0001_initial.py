# Generated by Django 3.2.18 on 2023-02-19 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Constituency code')),
                ('title', models.CharField(max_length=255, verbose_name='Constituency name')),
                ('details', models.TextField(blank=True, help_text='Details', null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', help_text='Constituency status', max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('agent', models.ForeignKey(blank=True, help_text='Agent in command', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'geo_constituency',
            },
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=25, verbose_name='Nation code')),
                ('title', models.CharField(max_length=255, verbose_name='Nation name')),
                ('agent', models.ForeignKey(blank=True, help_text='Agent in command', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'geo_nation',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Constituency name')),
                ('details', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('agent', models.ForeignKey(blank=True, help_text='Agent in command', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('constituency', models.ForeignKey(help_text='Constituency', on_delete=django.db.models.deletion.CASCADE, to='geo.constituency')),
            ],
            options={
                'db_table': 'geo_station',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Region name')),
                ('details', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('agent', models.ForeignKey(blank=True, help_text='Agent in command', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nation', models.ForeignKey(help_text='Nation', on_delete=django.db.models.deletion.CASCADE, to='geo.nation')),
            ],
            options={
                'db_table': 'geo_region',
            },
        ),
        migrations.AddField(
            model_name='constituency',
            name='region',
            field=models.ForeignKey(help_text='Region', on_delete=django.db.models.deletion.CASCADE, to='geo.region'),
        ),
    ]
