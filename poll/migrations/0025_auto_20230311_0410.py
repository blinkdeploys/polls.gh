# Generated by Django 3.2.18 on 2023-03-11 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0012_alter_agent_zone_ct'),
        ('geo', '0007_auto_20230307_0707'),
        ('poll', '0024_auto_20230307_0200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultsheet',
            name='constituency_agent',
        ),
        migrations.RemoveField(
            model_name='resultsheet',
            name='constituency_approved_at',
        ),
        migrations.RemoveField(
            model_name='resultsheet',
            name='nation_agent',
        ),
        migrations.RemoveField(
            model_name='resultsheet',
            name='national_approval_at',
        ),
        migrations.RemoveField(
            model_name='resultsheet',
            name='region_agent',
        ),
        migrations.RemoveField(
            model_name='resultsheet',
            name='regional_approval_at',
        ),
        migrations.AlterField(
            model_name='resultsheet',
            name='station_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_sheets', to='people.agent'),
        ),
        migrations.CreateModel(
            name='StationCollationSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField(blank=True, help_text='Total number of votes', null=True, verbose_name='EC Summary Collation totals')),
                ('total_valid_votes', models.IntegerField(blank=True, help_text='Total number of valid votes', null=True, verbose_name='Collation total number of valid votes')),
                ('total_invalid_votes', models.IntegerField(blank=True, help_text='Total number of invalid votes', null=True, verbose_name='Collation total number of invalid votes')),
                ('station_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Stational Approved At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35, null=True)),
                ('candidate', models.ForeignKey(blank=True, default=None, help_text='Candidate', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_collation_sheets', to='people.candidate')),
                ('station', models.ForeignKey(help_text='Polling Station', on_delete=django.db.models.deletion.CASCADE, related_name='station_collation_sheets', to='geo.station')),
                ('station_agent', models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_collation_sheets', to='people.agent')),
            ],
            options={
                'db_table': 'poll_station_collation_sheet',
            },
        ),
        migrations.CreateModel(
            name='RegionalCollationSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField(blank=True, help_text='Total number of votes', null=True, verbose_name='EC Summary Collation totals')),
                ('total_valid_votes', models.IntegerField(blank=True, help_text='Total number of valid votes', null=True, verbose_name='Collation total number of valid votes')),
                ('total_invalid_votes', models.IntegerField(blank=True, help_text='Total number of invalid votes', null=True, verbose_name='Collation total number of invalid votes')),
                ('regional_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Regional Approved At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35, null=True)),
                ('candidate', models.ForeignKey(blank=True, default=None, help_text='Candidate', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_collation_sheets', to='people.candidate')),
                ('region', models.ForeignKey(help_text='Region', on_delete=django.db.models.deletion.CASCADE, related_name='regional_collation_sheets', to='geo.region')),
                ('region_agent', models.ForeignKey(blank=True, default=None, help_text='Regional agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_collation_sheets', to='people.agent')),
            ],
            options={
                'db_table': 'poll_regional_collation_sheet',
            },
        ),
        migrations.CreateModel(
            name='NationalCollationSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField(blank=True, help_text='Total number of votes', null=True, verbose_name='EC Summary Collation totals')),
                ('total_valid_votes', models.IntegerField(blank=True, help_text='Total number of valid votes', null=True, verbose_name='Collation total number of valid votes')),
                ('total_invalid_votes', models.IntegerField(blank=True, help_text='Total number of invalid votes', null=True, verbose_name='Collation total number of invalid votes')),
                ('national_approval_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date of Regional Approved At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35, null=True)),
                ('candidate', models.ForeignKey(blank=True, default=None, help_text='Candidate', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='national_collation_sheets', to='people.candidate')),
                ('nation', models.ForeignKey(help_text='Nation', on_delete=django.db.models.deletion.CASCADE, related_name='national_collation_sheets', to='geo.nation')),
                ('nation_agent', models.ForeignKey(blank=True, default=None, help_text='National agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='national_collation_sheets', to='people.agent')),
            ],
            options={
                'db_table': 'poll_national_collation_sheet',
            },
        ),
        migrations.CreateModel(
            name='ConstituencyCollationSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.IntegerField(blank=True, help_text='Total number of votes', null=True, verbose_name='EC Summary Collation totals')),
                ('total_valid_votes', models.IntegerField(blank=True, help_text='Total number of valid votes', null=True, verbose_name='Collation total number of valid votes')),
                ('total_invalid_votes', models.IntegerField(blank=True, help_text='Total number of invalid votes', null=True, verbose_name='Collation total number of invalid votes')),
                ('constituency_approved_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Constituency Approved At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=35, null=True)),
                ('candidate', models.ForeignKey(blank=True, default=None, help_text='Candidate', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituency_collation_sheets', to='people.candidate')),
                ('constituency', models.ForeignKey(help_text='Constituency', on_delete=django.db.models.deletion.CASCADE, related_name='constituency_collation_sheets', to='geo.station')),
                ('constituency_agent', models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituency_collation_sheets', to='people.agent')),
            ],
            options={
                'db_table': 'poll_constituency_collation_sheet',
            },
        ),
    ]
