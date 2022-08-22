# Generated by Django 4.0.5 on 2022-08-22 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('short_description', models.TextField()),
                ('further_information', models.TextField(null=True)),
                ('reasons', models.TextField()),
                ('references', models.TextField(null=True)),
                ('category_url', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea_note', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea_name', models.CharField(max_length=200)),
                ('brief_description', models.TextField()),
                ('examples_application', models.TextField(null=True)),
                ('tool', models.TextField(null=True)),
                ('implementation_steps', models.TextField(null=True)),
                ('teacher_effort', models.TextField()),
                ('recommendations', models.TextField()),
                ('supplementary_material', models.TextField()),
                ('reusable', models.TextField(null=True)),
                ('testimony', models.TextField(null=True)),
                ('references', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlanCategoryOnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_category', to='tbcore.category')),
                ('idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_i', to='tbcore.onlineidea')),
                ('notes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_plan', to='tbcore.notes')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_plan', to='tbcore.plan')),
            ],
        ),
        migrations.AddField(
            model_name='notes',
            name='online_idea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_online_idea', to='tbcore.onlineidea'),
        ),
        migrations.CreateModel(
            name='CategoryOnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tbcore.category')),
                ('online_idea', models.ManyToManyField(to='tbcore.onlineidea')),
            ],
        ),
    ]
