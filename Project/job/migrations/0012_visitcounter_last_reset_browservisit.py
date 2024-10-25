# Generated by Django 4.1.7 on 2024-10-22 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitcounter',
            name='last_reset',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='BrowserVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser_id', models.CharField(max_length=100)),
                ('last_visit', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
            ],
            options={
                'unique_together': {('browser_id', 'ip_address')},
            },
        ),
    ]
