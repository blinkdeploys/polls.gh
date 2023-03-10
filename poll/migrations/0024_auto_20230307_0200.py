# Generated by Django 3.2.18 on 2023-03-07 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_alter_party_agent'),
        ('poll', '0023_alter_resultsheet_result_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='station_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Station agent that recorded the result', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='people.agent'),
        ),
        migrations.AlterField(
            model_name='resultapproval',
            name='approving_agent',
            field=models.ForeignKey(help_text='Agent that approved the result', on_delete=django.db.models.deletion.CASCADE, related_name='result_approvals', to='people.agent'),
        ),
        migrations.AlterField(
            model_name='resultsheet',
            name='constituency_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituency_result_sheets', to='people.agent'),
        ),
        migrations.AlterField(
            model_name='resultsheet',
            name='nation_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='National agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='national_result_sheets', to='people.agent'),
        ),
        migrations.AlterField(
            model_name='resultsheet',
            name='region_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Regional agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regional_result_sheets', to='people.agent'),
        ),
        migrations.AlterField(
            model_name='resultsheet',
            name='station_agent',
            field=models.ForeignKey(blank=True, default=None, help_text='Constituency agent that recorded results', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='station_result_sheets', to='people.agent'),
        ),
    ]
