# Generated by Django 5.1.1 on 2024-09-15 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_demodata_user_payment_imagesubmission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_status',
            field=models.BooleanField(default=False),
        ),
    ]
