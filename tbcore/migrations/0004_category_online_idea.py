from django.db import migrations

def create_category_online_idea (apps,schema_editor ):
    Category = apps.get_model('tbcore', 'Category')
    OnlineIdea = apps.get_model('tbcore', 'OnlineIdea')
    CategoryOnlineIdea = apps.get_model('tbcore', 'CategoryOnlineIdea')

    #create CategoryOnlineIdea objects

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Human Touch')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Short Student Introduction/ 2 Truths one lie'),
        OnlineIdea.objects.get(idea_name='Instructor introduction video'),
        OnlineIdea.objects.get(idea_name='Share stories and experiences with students')
    )

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Organization')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Syllabus'),
        OnlineIdea.objects.get(idea_name='Weekly emails/ periodic communication'))

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assignments')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Reflection portfolio'),
        OnlineIdea.objects.get(idea_name='Peer Review'))


def undo_create_category_online_idea(apps, schema_editor):
    CategoryOnlineIdea = apps.get_model('tbcore', 'CategoryOnlineIdea')
    CategoryOnlineIdea.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tbcore', '0003_online_ideas'),
    ]
    operations = [
        migrations.RunPython(create_category_online_idea, undo_create_category_online_idea)
    ]




