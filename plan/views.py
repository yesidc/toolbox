from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from .helpers import category_done, is_ajax, context_summary
from tbcore.models import *
from .forms import NotesForm, PlanForm
import json

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


def get_ideas(user, category_url, current_user_plan_id):
    """
    Fetches all ideas that belong to a particular user, plan and category from PlanCategoryOnlineIdea object.
    """

    if user.is_anonymous:
        return None
    else:
        idea_list = [i.idea.id for i in PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=user) & Q(plan__pk=current_user_plan_id) & Q(
                category__category_url=category_url))]
        return idea_list


# todo move to a helpers.py module. There should only be views definitions here
def get_category(category_url):
    # todo cache this information, as the output is always the same
    # holds the name of the current building block or category
    GLOBAL_CONTEXT['current_category'] = category_url
    # There are a total of eight building blocks hence 8 CategoryOnlineIdea objects.
    return CategoryOnlineIdea.objects.get(category__category_url=category_url)


# todo use get_object_or_404() function with all the category_block_name variable

def show_block(request, category_url, next_page):
    if 'current_user_plan' in request.session:
        ideas_list = get_ideas(request.user, category_url, request.session['current_user_plan'])
    else:
        ideas_list = None
    context = {'category': get_category(category_url),
               'next_page': next_page,
               'ideas_list': ideas_list, }
    context.update(GLOBAL_CONTEXT)

    return render(request, 'plan/block_content.html', context=context, )

# def human_touch(request):
#     context = {'category': get_category('human_touch'),
#                'next_page': 'teaching_material',
#                'name_next_page': 'Teaching Material',
#                'ideas_list': get_ideas(request.user, 'human_touch',request.session['current_user_plan']), }
#     context.update(GLOBAL_CONTEXT)
#
#     return render(request, 'plan/block_content.html', context=context, )


def idea_overview_detail(request, category_name, idea_id, detailed_view):
    current_idea = get_object_or_404(OnlineIdea, id=idea_id)
    # This idea id is used when saving the idea to a PlanCategoryOnlineIdea Object
    GLOBAL_CONTEXT['current_idea'] = current_idea.pk
    if GLOBAL_CONTEXT['current_category'] is None:
        GLOBAL_CONTEXT['current_category'] = Category.objects.get(category_name=category_name)

    note_form = NotesForm()
    try:
        pcoi_obj = PlanCategoryOnlineIdea.objects.get(
            plan=Plan.objects.get(plan_name=GLOBAL_CONTEXT['current_user_plan']),
            category=Category.objects.get(category_url=GLOBAL_CONTEXT['current_category']),
            idea=OnlineIdea.objects.get(pk=GLOBAL_CONTEXT['current_idea']),

        )
        note_form = NotesForm(initial={'note_content': pcoi_obj.notes})
    except:
        pcoi_obj = None

    context = {
        'idea': current_idea,
        'note_form': note_form
    }
    context.update(GLOBAL_CONTEXT)

    # handles all logic when user adds idea or/and note from the idea_detail page
    if request.method == "POST":

        note_form = NotesForm(request.POST)
        if note_form.is_valid():
            if pcoi_obj is None:
                pcoi_obj = PlanCategoryOnlineIdea.objects.create(
                    plan=Plan.objects.get(plan_name=GLOBAL_CONTEXT['current_user_plan']),
                    category=Category.objects.get(category_url=GLOBAL_CONTEXT['current_category']),
                    idea=OnlineIdea.objects.get(pk=GLOBAL_CONTEXT['current_idea']),

                )

            pcoi_obj.notes = note_form.cleaned_data['note_content']
            pcoi_obj.save()

        return redirect(GLOBAL_CONTEXT['current_category'])

    # manages get request
    if detailed_view == 'detailed_view':

        return render(request, 'plan/idea_detail.html', context=context)
    else:
        # todo this is where get request are handled, here is it where saved notes are displayed.
        return render(request, 'plan/idea_overview.html', context=context)


@login_required
def checklist(request):
    c_s, c_d = context_summary(request.user, GLOBAL_CONTEXT['current_user_plan'])
    context = {
        'context_summary': c_s,
        'category_done_summary': c_d
    }
    return render(request, 'plan/checklist.html', context=context)


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
                new_plan.save()
                request.session['current_user_plan'] = new_plan.pk


        except IntegrityError:
            # todo implment django messages

            messages.add_message(request, messages.INFO, 'This plan already exists')

    # When user logs in, is prompted to create a course/plan by being redirected to a form, this if statement handles
    # it.
    if start_add == 'get_started':
        if request.method == "POST":
            plan_to_database()

            return redirect('human_touch')
        try:
            # if user does not fill out the form to create a new course/plan, the current plan/course
            # is default to the last course the user created.
            request.session['current_user_plan'] = Plan.objects.select_related('user').filter(
                user=request.user).last().pk
        except AttributeError:
            # occurs when user has no plans in database, hence needs to add at least one to be able to save idea and
            # notes.
            request.session['current_user_plan'] = None

        return render(request, 'plan/course_name.html', context=context)
    elif start_add == 'add_new_plan':
        if request.method == "POST":
            plan_to_database()
            # user redirected to previous page
            return redirect(request.META.get('HTTP_REFERER'))


@login_required
def use_idea(request, save_note=None):
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
            Q(plan__user=request.user) & Q(plan__plan_name=GLOBAL_CONTEXT['current_user_plan']) & Q(
                category__category_url=GLOBAL_CONTEXT['current_category']) & Q(
                idea__pk=GLOBAL_CONTEXT['current_idea']))[0].delete()
        # todo add to sessions as this is also computed in select_plan view
        # categories for which user has already selected at least one idea
        category_ready = category_done(GLOBAL_CONTEXT['current_user_plan'])
        # messages.info(request, 'Idea successfully deleted from your plan')
        json_dic = {
            'category_ready': list(category_ready),
            "category_id": GLOBAL_CONTEXT['current_category'],
            'plan_id': GLOBAL_CONTEXT['current_user_plan'].pk
        }
        return JsonResponse(json_dic)


    else:
        # prevents user from saving the same ideas twice for the same course plan.
        try:
            PlanCategoryOnlineIdea.objects.create(
                plan=Plan.objects.get(plan_name=GLOBAL_CONTEXT['current_user_plan']),
                category=Category.objects.get(category_url=GLOBAL_CONTEXT['current_category']),
                idea=OnlineIdea.objects.get(pk=GLOBAL_CONTEXT['current_idea']),

            )

            # messages.add_message(request, messages.ERROR, 'Idea successfully added to your plan')

        except IntegrityError:

            messages.add_message(request, messages.INFO, 'This idea has been already added to you course plan')
            return redirect(request.META.get('HTTP_REFERER'))
    # return redirect( GLOBAL_CONTEXT['current_category'])

    json_dic = {
        "category_id": GLOBAL_CONTEXT['current_category'],
        'plan_id': GLOBAL_CONTEXT['current_user_plan'].pk
    }
    # if user has either deleted or added an idea using the checkboxes on the blocks/category page
    if is_ajax(request):
        return JsonResponse(json_dic)
    else:
        # if user has selected and idea using the buttons provided by both the overview or detail idea page.
        return redirect(GLOBAL_CONTEXT['current_category'])


def delete_pcoi_checklist(request):
    """
    Manages all related to deleting PlanCategoryOnlineIdea objects when users interact with the checklist page
    """

    PlanCategoryOnlineIdea.objects.get(pk=request.GET.get('pcoi_id')).delete()
    return JsonResponse({}, status=200)


def select_plan(request):
    """
    Triggered when user chooses to work on a different plan. User can switch to a
    different plan using the navigation bar on the left.
    """
    # update current_user_plan stored in sessions.
    request.session['current_user_plan'] = request.GET.get('plan_id')

    current_user_plan = Plan.objects.get(pk=request.GET.get('plan_id'))
    # categories for which user has already selected at least one idea
    category_ready = category_done(current_user_plan)

    response_dict = {
        'category_ready': list(category_ready),
        # this is the name that is shown on the top right (Name is changed dynamically through the DOM)
        'plan_name_ajax': current_user_plan.plan_name,
        # this is the id assigned to the div element that contains all blocks/categories on the sidebar
        'plan_id_response': request.GET.get('plan_id')
    }

    return JsonResponse(response_dict)



def update_selected_idea(request):
    """
    Updates the content of the block_content page such that when the user switches to a different course/plan using
    the side navigation bar, the ticked-off ideas reflect that of the current chosen plan/course
    """
    context = {'category': get_category(GLOBAL_CONTEXT['current_category']),
               'ideas_list': get_ideas(request.user, GLOBAL_CONTEXT['current_category'], request.session['current_user_plan'])
               }
    context.update(GLOBAL_CONTEXT)
    return render(request, 'plan/update_ideas.html', context=context)
