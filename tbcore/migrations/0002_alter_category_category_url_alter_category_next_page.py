# Generated by Django 4.0.5 on 2022-12-20 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_url',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='next_page',
            field=models.SlugField(null=True),
        ),
    ]
