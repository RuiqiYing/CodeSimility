# Generated by Django 4.0.4 on 2023-02-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_questionbank_optiona_questionbank_optionb_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionbank',
            name='optionA',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='questionbank',
            name='optionB',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='questionbank',
            name='optionC',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='questionbank',
            name='optionD',
            field=models.TextField(max_length=10000),
        ),
    ]
