# Generated by Django 4.0.3 on 2022-08-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankmodel',
            name='name',
            field=models.CharField(max_length=255, verbose_name='نام بانک'),
        ),
    ]
