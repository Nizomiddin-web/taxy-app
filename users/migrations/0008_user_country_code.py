# Generated by Django 5.1.1 on 2024-09-16 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_facecheck_machinecheck_delete_imagesubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Mamlakat Kodi'),
        ),
    ]
