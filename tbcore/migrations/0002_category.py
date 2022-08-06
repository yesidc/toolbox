from django.db import migrations


def create_category(apps, schema_editor):
    Category = apps.get_model('tbcore', 'Category')
    # create categories

    human_touch = Category.objects.create(
        category_name='Human Touch',
        short_description='Human Touch arises by talking about topics that are not directly related to the topic of '
                          'the course but may be related to the students’ extracurricular activities, '
                          'social engagement in the study program and ideas for courses or study projects.  Hallway '
                          'chatter concerns discussions about thesis topics, students bringing up that they wrote '
                          'an article about a particular robot or that they want to download an article but they '
                          'are facing a paywall. Further, there are things you don’t want to be recorded as a '
                          'lecturer, e.g. talking about unofficial news.',
        reasons='The social dimension and social interaction can be seen as predecessors for understanding. Knowing '
                'the people of the course greatly helps to manage uncertainty about participation and comprehension '
                'questions. Especially the CogSci student body is very active and engaged to give everyone the same '
                'opportunity and this should apply to all students, on-site and online. '

    )
    teaching_material = Category.objects.create(
        category_name='Teaching Material',
        short_description='The teaching material constitutes the basis of the study material. It covers all necessary sources for meeting the learning goals, which also includes additional explanations that make topics more tangible or comprehendable. If synchronous discussions comprise an essential part of the learning material, then they must be accessible to online students as well. Therefore, for online courses ',
        reasons='Since the COSMOS-program opened the Cognitive Science Master for online students students from any time zone, any single and synchronous time slot for lecture meetings on-site or online would exclude one of the students. ',

    )
    organization = Category.objects.create(
        category_name='Organization',
        short_description="<h5>Give complete, exact information (incl. teaching mode) available at the start of the semester:<h5>"
        "<br>"
        "<h6>Course information:</h6>"
        "<ul>"
                
                "<li>Meeting days and time for courses with synchronous meetings</li>"
                "<li>Instructional modality, as a way to help students understand how the course is designed </li>"
                "<li>ECTS</li>"
                "<li>Please list the prerequisites concisely, i.e. in a way that students can check if they need to brush up the prerequisites (i.e. „linear algebra“ is too vague). You can list UOS or external courses that cover the prerequisites.</li>"
                "<li>Teaching staff contact information</li>"
                "<li>Course description</li>"
                "<li>Learning resources, technology and texts</li>"
                "<li>Learning outcome (i.e. after taking the course, you can...) / course goals or scope of the course</li>"
                "<li>Assignments</li>"
                "<li>Grading scale</li>"
        "</ul>",



        reasons=' Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',

    )
    assignment = Category.objects.create(
        category_name='Assignments',
        short_description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',
        reasons='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',

    )
    discussion = Category.objects.create(
        category_name='Discussion',
        short_description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',
        reasons='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia ',

    )
    student_engagement = Category.objects.create(
        category_name='Student Engagement',
        short_description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',
        reasons='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',

    )
    assessment = Category.objects.create(
        category_name='Assessment',
        short_description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',
        reasons='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia ',

    )
    rules_regulations = Category.objects.create(
        category_name='Rules & Regulations',
        short_description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',
        reasons=' Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia',

    )


def undo_category(apps, schema_editor):
    Category = apps.get_model('tbcore', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tbcore', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_category, undo_category)
    ]
