# Generated by Django 5.1.1 on 2024-09-20 04:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('daily', 'Kunlik'), ('monthly', 'Oylik'), ('weekly', 'Haftalik'), ('yearly', 'Yillik')], max_length=10, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.amount'),
        ),
    ]
