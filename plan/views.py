import sqlite3

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from tbcore.models import *
from .forms import NotesForm, PlanForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
# todo optimize database queries,ex. create 500 users and evaluate performance


# todo having a global context causes the migrations error Operational error. Since these lines of
# todo are run before the migration operation is executed.
GLOBAL_CONTEXT = {
    'current_user_plan': None,  # the plan users works on
    'form': PlanForm(),
    'current_category': None,
    'current_idea': None
}


def get_ideas(user, category_url):
    """
    Fetches all ideas that belong to a particular user, plan and category from PlanCategoryOnlineIdea object.
    """

    if user.is_anonymous:
        return None
    else:
        idea_list = [i.idea.id for i in PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=user) & Q(plan__plan_name=GLOBAL_CONTEXT['current_user_plan']) & Q(
                category__category_url=category_url))]
        return idea_list


# todo move to a helpers.py module. There should only be views definitions here
def get_category(category_url):
    # todo you can also cache this information
    # holds the name of the current building block or category
    GLOBAL_CONTEXT['current_category'] = category_url
    return CategoryOnlineIdea.objects.get(category__category_url=category_url)


# todo use get_object_or_404() function with all the category_block_name variable

def human_touch(request):
    context = {'category': get_category('human_touch'),
               'next_page': 'teaching_material',
               'name_next_page': 'Teaching Material',
               'ideas_list': get_ideas(request.user, 'human_touch')}
    context.update(GLOBAL_CONTEXT)

    return render(request, 'plan/block_content.html', context=context)


def teaching_material(request):
    # category_teaching_material = CategoryOnlineIdea.objects.get(category__category_name='Teaching Material')
    # GLOBAL_CONTEXT['current_category'] = 'teaching_material'
    context = {'category': get_category('teaching_material'),
               'next_page': 'organization',
               'name_next_page': 'Organization',
               'ideas_list': get_ideas(request.user, 'teaching_material')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def organization(request):
    # category_organization = CategoryOnlineIdea.objects.get(category__category_name='Organization')
    # GLOBAL_CONTEXT['current_category'] = 'organization'
    context = {'category': get_category('organization'),
               'next_page': 'assignment',
               'name_next_page': 'Assignment',
               'ideas_list': get_ideas(request.user, 'organization')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def assignment(request):
    # category_assignmet = CategoryOnlineIdea.objects.get(category__category_name='Assignments')
    # GLOBAL_CONTEXT['current_category'] = 'assignment'
    context = {'category': get_category('assignment'),
               'next_page': 'discussion',
               'name_next_page': 'Discussion',
               'ideas_list': get_ideas(request.user, 'assignment')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def discussion(request):
    # category_discussion = CategoryOnlineIdea.objects.get(category__category_name='Discussion')
    # GLOBAL_CONTEXT['current_category'] = 'discussion'
    context = {'category': get_category('discussion'),
               'next_page': 'student_engagement',
               'name_next_page': 'Student Engagement',
               'ideas_list': get_ideas(request.user, 'assignment')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def student_engagement(request):
    # category_student_engagement = CategoryOnlineIdea.objects.get(category__category_name='Student Engagement')
    # GLOBAL_CONTEXT['current_category'] = 'student_engagement'
    context = {'category': get_category('student_engagement'),
               'next_page': 'assessment',
               'name_next_page': 'Assessment',
               'ideas_list': get_ideas(request.user, 'student_engagement')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def assessment(request):
    # category_assessment = CategoryOnlineIdea.objects.get(category__category_name='Assessment')
    # GLOBAL_CONTEXT['current_category'] = 'assessment'
    context = {'category': get_category('assessment'),
               'next_page': 'rules_regulations',
               'name_next_page': 'Rules & Regulations',
               'ideas_list': get_ideas(request.user, 'assessment')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def rules_regulations(request):
    # category_rules_regulations = CategoryOnlineIdea.objects.get(category__category_name='Rules & Regulations')
    # GLOBAL_CONTEXT['current_category'] = 'rules_regulations'
    context = {'category': get_category('rules_regulations'),
               'ideas_list': get_ideas(request.user, 'rules_regulations')}
    context.update(GLOBAL_CONTEXT)
    # context['current_user_plan'] = get_latest_plan(request.user,context['current_user_plan'])
    return render(request, 'plan/block_content.html', context=context)


def idea_overview_detail(request, category_name, idea_id, detailed_view):
    update = False
    current_idea = get_object_or_404(OnlineIdea, id=idea_id)
    # This idea id is used when saving the idea to a PlanCategoryOnlineIdea Object
    GLOBAL_CONTEXT['current_idea'] = current_idea.pk
    context = {
        'idea': current_idea,

    }
    context.update(GLOBAL_CONTEXT)
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


def checklist(request):
    return render(request, 'plan/checklist.html')


@login_required
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
        """
        Validates form data and saves them to the database.
        """

        try:
            form = PlanForm(request.POST)
            if form.is_valid():
                new_plan = form.save(commit=False)
                new_plan.user = User.objects.get(username=request.user)
                GLOBAL_CONTEXT['current_user_plan'] = new_plan

                new_plan.save()
        except IntegrityError:
            # todo implment django messages

            messages.add_message(request, messages.INFO, 'This plan already exists')

    # When user logs in, is prompted to create a course/plan by being redirected to a form, thi if statement handles it.
    if start_add == 'get_started':
        if request.method == "POST":
            plan_to_database()

            return redirect('human_touch')

        # if user does not fill out the form to create a new course/plan, the current plan/course
        # is default to the last course the user created.
        GLOBAL_CONTEXT['current_user_plan'] = plans = Plan.objects.select_related('user').filter(
            user=request.user).last()
        return render(request, 'plan/course_name.html', context=context)
    elif start_add == 'add_new_plan':
        if request.method == "POST":
            plan_to_database()
            # user redirected to previous page
            return redirect(request.META.get('HTTP_REFERER'))


@login_required
def use_idea(request):
    # todo this should be into a try method, or return and 404 error. IF the server is reloaed the GLOBAL_CONTEXT IS LOST AND the OBJECT below cannot be created
    # todo there should not be repeated objects, use Unique.

    GLOBAL_CONTEXT['current_idea'] = request.GET.get('idea_id') or GLOBAL_CONTEXT['current_idea']
    # If there's no plan in the GLOBAL_CONTEXT dictionary; grab the plan name from the DOM
    GLOBAL_CONTEXT['current_user_plan'] = GLOBAL_CONTEXT['current_user_plan'] or request.GET.get('plan_name_dom')

    # If the system lost track of the current idea or category e.g., the server crashed; these are extracted from the
    # current URL
    if GLOBAL_CONTEXT['current_idea'] is None:
        GLOBAL_CONTEXT['current_idea'] = request.META.get('HTTP_REFERER').split('/')[4]
    elif GLOBAL_CONTEXT['current_category'] is None:
        GLOBAL_CONTEXT['current_category'] = request.META.get('HTTP_REFERER').split('/')[3]

    if request.GET.get('delete_idea'):
        # Delete object
        PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=request.user) & Q(plan__plan_name=GLOBAL_CONTEXT['current_user_plan']) &
            Q(category__category_url=GLOBAL_CONTEXT['current_category']) & Q(
                idea__pk=GLOBAL_CONTEXT['current_idea'])).delete()
    else:
        # prevents user from saving the same ideas twice for the same course plan.
        try:
            PlanCategoryOnlineIdea.objects.create(
                plan=Plan.objects.get(plan_name=GLOBAL_CONTEXT['current_user_plan']),
                category=Category.objects.get(category_url=GLOBAL_CONTEXT['current_category']),
                idea=OnlineIdea.objects.get(pk=GLOBAL_CONTEXT['current_idea']),

            )
        except IntegrityError:

            messages.add_message(request, messages.INFO, 'This idea has been already added to you course plan')
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(GLOBAL_CONTEXT['current_category'])


def select_plan(request):
    """
    Triggered when user chooses to work on a different plan. User can switch to a
    different plan using the navigation bar on the left.
    """
    GLOBAL_CONTEXT['current_user_plan'] = Plan.objects.get(plan_name=request.GET.get('plan_name').replace('-',' '))

    plan_name_ajax = GLOBAL_CONTEXT['current_user_plan'].plan_name
    return JsonResponse({'plan_name_ajax':plan_name_ajax}, status=200)

