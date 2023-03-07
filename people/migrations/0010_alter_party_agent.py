# Generated by Django 3.2.18 on 2023-03-07 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0009_alter_agent_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='agent',
            field=models.ForeignKey(blank=True, help_text='Agent in command', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parties', to='people.agent'),
        ),
    ]