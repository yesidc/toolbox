# Generated by Django 4.0.5 on 2024-06-15 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tbcore', '0002_rename_short_description_category_description_1_and_more_alter_onlineidea_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_start_page',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='CategoryOnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tbcore.category')),
                ('idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbcore.onlineidea')),
            ],
        ),
    ]
