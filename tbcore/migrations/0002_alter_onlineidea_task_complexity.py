# Generated by Django 4.0.5 on 2022-11-30 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineidea',
            name='task_complexity',
            field=models.IntegerField(null=True),
        ),
    ]