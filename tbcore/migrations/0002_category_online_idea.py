from django.db import migrations

def create_category_online_idea (apps,schema_editor ):
    Category = apps.get_model('tbcore', 'Category')
    OnlineIdea = apps.get_model('tbcore', 'OnlineIdea')
    CategoryOnlineIdea = apps.get_model('tbcore', 'CategoryOnlineIdea')

    #create CategoryOnlineIdea objects

    CategoryOnlineIdea.objects.bulk_create([
        #Human Touch






    ])

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

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Teaching Material')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Micro Lectures'),
        )


    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Discussion')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Make yourself available')
       )

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Student Engagement')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Make yourself available') #todo this does not belong here
       )

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assessment')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Oral exam')
    )

    CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Rules & Regulations')).online_idea.add(
        OnlineIdea.objects.get(idea_name='Matches module description')
    )





def undo_create_category_online_idea(apps, schema_editor):
    CategoryOnlineIdea = apps.get_model('tbcore', 'CategoryOnlineIdea')
    CategoryOnlineIdea.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tbcore', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_category_online_idea, undo_create_category_online_idea)
    ]




