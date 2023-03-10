# Generated by Django 3.2.18 on 2023-02-20 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='level',
            field=models.IntegerField(choices=[(0, 'Unassigned'), (1, 'Station'), (2, 'Constituency'), (3, 'Region'), (4, 'National')], default=0, max_length=4, verbose_name='Office level'),
        ),
    ]
