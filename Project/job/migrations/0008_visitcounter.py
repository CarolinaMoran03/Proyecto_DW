# Generated by Django 4.1.7 on 2024-10-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_alter_job_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]