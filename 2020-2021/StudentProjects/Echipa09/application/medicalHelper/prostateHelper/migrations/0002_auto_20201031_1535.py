# Generated by Django 3.1.2 on 2020-10-31 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prostateHelper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='confidence',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
    ]
