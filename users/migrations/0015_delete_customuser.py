# Generated by Django 5.1.1 on 2024-09-20 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
