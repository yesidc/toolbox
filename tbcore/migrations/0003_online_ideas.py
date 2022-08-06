from django.db import migrations


def create_online_ideas(apps, schema_editor):
    OnlineIdea = apps.get_model ('tbcore','OnlineIdea')

    student_intro = OnlineIdea.objects.create(
        idea_name= 'Short Student Introduction/ 2 Truths one lie',
        description = 'Students write a short introduction/ description about themselves. The topic or focus is free for them to choose, so they can write something authentic about themselves with which they feel comfortable sharing. This way, course participants get a feel for who else is in the course and what they are interested in. The point is to make the course human, so students can write anything that shows they are not an AI This is a gamified approach! Students can write anything about their background or even come up with a funny story about themselves that mustn Alternatively, everyone shares 2 truths and one lie about themselves. ',
        short_description = "<ul>"
                                "<li> Microlectures: spice up your micro lectures with an anecdote </li>"
                                "<li> Courseware: you can use the explanatory texts and the design of the pages and sections to share stories or experiences which relate to the presented material. THis can give our whole courseware a new flavor, even if you do it only in a few instances. </li>"
                            "</ul>",

        implementation_steps = 'Lorem ipsum dolor sit amet consectetur',
        teacher_effort = 'Lorem ipsum dolor sit amet consectetur',
        recommendations = 'Lorem ipsum dolor sit amet consectetur',
        supplementary_material = 'Lorem ipsum dolor sit amet consectetur',
        examples_application = 'Lorem ipsum dolor sit amet consectetur',
        testimony = 'Lorem ipsum dolor sit amet consectetur',
        references = 'Lorem ipsum dolor sit amet consectetur'
    )
    # student_intro = OnlineIdea.objects.create(
    #     idea_name= ,
    #     description = ,
    #     short_description = ,
    #
    #     implementation_steps = ,
    #     teacher_effort = ,
    #     recommendations = ,
    #     supplementary_material = ,
    #     examples_application = ,
    #     testimony = ,
    #     references =
    # )
    # student_intro = OnlineIdea.objects.create(
    #     idea_name= ,
    #     description = ,
    #     short_description = ,
    #
    #     implementation_steps = ,
    #     teacher_effort = ,
    #     recommendations = ,
    #     supplementary_material = ,
    #     examples_application = ,
    #     testimony = ,
    #     references =
    # )
    # student_intro = OnlineIdea.objects.create(
    #     idea_name= ,
    #     description = ,
    #     short_description = ,
    #
    #     implementation_steps = ,
    #     teacher_effort = ,
    #     recommendations = ,
    #     supplementary_material = ,
    #     examples_application = ,
    #     testimony = ,
    #     references =
    # )
    # student_intro = OnlineIdea.objects.create(
    #     idea_name= ,
    #     description = ,
    #     short_description = ,
    #
    #     implementation_steps = ,
    #     teacher_effort = ,
    #     recommendations = ,
    #     supplementary_material = ,
    #     examples_application = ,
    #     testimony = ,
    #     references =
    # )

def undo_online_ideas (apps, schema_editor):
    OnlineIdea = apps.get_model('tbcore', 'OnlineIdea')
    OnlineIdea.objects.all().delete()

class Migration (migrations.Migration):
    dependencies = [
        ('tbcore', '0002_category'),
    ]
    operations = [
        migrations.RunPython(create_online_ideas, undo_online_ideas)
    ]