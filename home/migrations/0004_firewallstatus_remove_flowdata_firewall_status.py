# Generated by Django 5.1.4 on 2024-12-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_flowdata_firewall_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirewallStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('status', models.CharField(default=None, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='flowdata',
            name='firewall_status',
        ),
    ]
