from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from tbcore.models import *
from .forms import NotesForm, PlanForm
import pdb

# Create your views here.


IDEA_PROPERTIES = ('idea_name', 'brief_description', 'examples_application',
                   'tool', 'implementation_steps', 'teacher_effort',
                   'recommendations', 'supplementary_material', 'reusable',
                   'testimony', 'references')

GLOBAL_CONTEXT ={}


def get_category(category_url):
    # todo you can also cache this information
    # holds the name of the current building block or category
    GLOBAL_CONTEXT['current_category'] = category_url
    return CategoryOnlineIdea.objects.get(category__category_url=category_url)



# todo use get_object_or_404() function with all the category_block_name variable

def human_touch(request):
    #category_human_touch = get_category('Human Touch')
    #GLOBAL_CONTEXT['current_category']= 'human_touch'

    context = {'category': get_category('human_touch'),
               'next_page': 'teaching_material',
               'name_next_page': 'Teaching Material'}
    return render(request, 'plan/block_content.html', context=context)


def teaching_material(request):
    #category_teaching_material = CategoryOnlineIdea.objects.get(category__category_name='Teaching Material')
    #GLOBAL_CONTEXT['current_category'] = 'teaching_material'
    context = {'category': get_category('teaching_material'),
               'next_page': 'organization',
               'name_next_page': 'Organization'}
    return render(request, 'plan/block_content.html', context=context)


def organization(request):
    #category_organization = CategoryOnlineIdea.objects.get(category__category_name='Organization')
    #GLOBAL_CONTEXT['current_category'] = 'organization'
    context = {'category': get_category('organization'),
               'next_page': 'assignment',
               'name_next_page': 'Assignment'}
    return render(request, 'plan/block_content.html', context=context)


def assignment(request):
    #category_assignmet = CategoryOnlineIdea.objects.get(category__category_name='Assignments')
    #GLOBAL_CONTEXT['current_category'] = 'assignment'
    context = {'category':get_category('assignment'),
               'next_page': 'discussion',
               'name_next_page': 'Discussion'}
    return render(request, 'plan/block_content.html', context=context)


def discussion(request):
    #category_discussion = CategoryOnlineIdea.objects.get(category__category_name='Discussion')
    #GLOBAL_CONTEXT['current_category'] = 'discussion'
    context = {'category': get_category('discussion'),
               'next_page': 'student_engagement',
               'name_next_page': 'Student Engagement'}
    return render(request, 'plan/block_content.html', context=context)


def student_engagement(request):
    #category_student_engagement = CategoryOnlineIdea.objects.get(category__category_name='Student Engagement')
    #GLOBAL_CONTEXT['current_category'] = 'student_engagement'
    context = {'category': get_category('student_engagement'),
               'next_page': 'assessment',
               'name_next_page': 'Assessment'}
    return render(request, 'plan/block_content.html', context=context)


def assessment(request):
    #category_assessment = CategoryOnlineIdea.objects.get(category__category_name='Assessment')
    #GLOBAL_CONTEXT['current_category'] = 'assessment'
    context = {'category': get_category('assessment'),
               'next_page': 'rules_regulations',
               'name_next_page': 'Rules & Regulations'}
    return render(request, 'plan/block_content.html', context=context)


def rules_regulations(request):
    #category_rules_regulations = CategoryOnlineIdea.objects.get(category__category_name='Rules & Regulations')
    #GLOBAL_CONTEXT['current_category'] = 'rules_regulations'
    context = {'category': get_category('rules_regulations')}
    return render(request, 'plan/block_content.html', context=context)


def idea_overview_detail(request, idea_id, detailed_view):
    update = False
    current_idea = get_object_or_404(OnlineIdea, id=idea_id)
    GLOBAL_CONTEXT['current_idea']= current_idea
    context = {
        'idea': current_idea,

    }
    if detailed_view == 'detailed_view':
        try:
            instance_note = current_idea.note_online_idea.all()[0]
            form = NotesForm(
                instance=instance_note)  # todo needs generalize to the case where there are many notes for an online idea
            update = True
        except IndexError:
            form = NotesForm()

        context['form'] = form
        if request.method == 'POST':
            form = NotesForm(request.POST, instance=instance_note) if update else NotesForm(request.POST)
            if form.is_valid():
                new_note = form.save(commit=False)
                new_note.online_idea = current_idea
                new_note.save()

            # updates the form with the new note
            context['form'] = NotesForm(instance=current_idea.note_online_idea.all()[0])
            # pdb.set_trace()
        return render(request, 'plan/idea_detail.html', context=context)
    else:
        # todo this is where get request are handled, here is it where saved notes are displayed.
        return render(request, 'plan/idea_overview.html', context=context)


# def idea_detail(request):
#     return render(request, 'plan/idea_detail.html')


def summary(request):
    return render(request, 'plan/summary.html')


# todo user needs to be logged in
def create_plan(request, start_add):
    """
    Triggered when user creates a new Plan
    Args:
        start_add: the template to be rendered depends on whether the user has just logged in or adds a new plan/course
    """
    form = PlanForm()
    context = {
        'form': form
    }
    def plan_to_database():
        form = PlanForm(request.POST)
        if form.is_valid():
            new_plan = form.save(commit=False)
            new_plan.user = User.objects.get(username=request.user)
            GLOBAL_CONTEXT['new_plan'] = new_plan

            new_plan.save()

    if start_add == 'get_started':
        if request.method == "POST":
            plan_to_database()



            return redirect('human_touch')

        return render(request, 'plan/course_name.html', context=context)
    elif start_add ==  'add_new_plan':
        if request.method == "POST":
            plan_to_database()
        return render (request, 'plan/base_block.html', context=context)


def use_idea(request):

#todo this should be into a try method, or return and 404 error. IF the server is reloaed the GLOBAL_CONTEXT IS LOST AND the OBJECT below cannot be created
    PlanCategoryOnlineIdea.objects.create(
        plan= GLOBAL_CONTEXT['new_plan'],
        category= Category.objects.get(category_url=GLOBAL_CONTEXT['current_category']),
        idea = GLOBAL_CONTEXT['current_idea'],

    )


    return redirect(GLOBAL_CONTEXT['current_category'])

