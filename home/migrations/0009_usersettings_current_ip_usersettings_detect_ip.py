# Generated by Django 5.1.4 on 2025-01-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_usersettings_allowed_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='current_ip',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='detect_ip',
            field=models.BooleanField(default=False),
        ),
    ]