# Generated by Django 5.1.5 on 2025-01-26 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=255),
        ),
    ]
