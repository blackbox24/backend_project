# Generated by Django 5.2.4 on 2025-07-30 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=3)),
                ('category', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['created_at'], name='expense_exp_created_b35aca_idx'), models.Index(fields=['name'], name='expense_exp_name_e2d612_idx')],
            },
        ),
    ]
