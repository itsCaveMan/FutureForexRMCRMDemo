# Generated by Django 2.2.16 on 2021-07-09 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_userprofile_assigned_categoryitems_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_performance_percentage_string',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
