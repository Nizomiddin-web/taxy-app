# Generated by Django 5.1.1 on 2024-09-15 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_email_customuser_sms_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ismi')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Familiyasi')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Telefon raqami')),
                ('verify_code', models.IntegerField(blank=True, null=True, verbose_name='SMS CODE')),
                ('verification_status', models.CharField(default='unverified', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_type', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='ImageSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='submissions/')),
                ('status', models.CharField(default='pending', max_length=20)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
