from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Count
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .helpers import category_done, is_ajax, context_summary, get_category, get_ideas, has_plan
from tbcore.models import *
from .forms import NotesForm, PlanForm
from tbcore.utils.create_pdf import render_pdf


from django.views.generic.base import TemplateView




# todo optimize database queries,ex. create 500 users and evaluate performance


# todo use get_object_or_404() function with all the category_block_name variable

def show_block(request, category_url, next_page):
    """
    Manages the content for all building blocks/categories.

    """
    request.session['current_category'] = category_url
    request.session['current_next_page'] = next_page
    if 'current_user_plan' in request.session:
        ideas_list = get_ideas(request.user, category_url, request.session['current_user_plan'])
    else:
        ideas_list = None

    category, instance_type = get_category(category_url) # a CategoryOnlineIdea instance

    context = {'category': category,
               'instance_type': instance_type,
               'next_page': next_page,
               'ideas_list': ideas_list,
               'current_category': category_url,
               'plan_form': PlanForm()} # User utilizes this form to create new plans/courses. Form available in all block pages.

    return render(request, 'plan/block_content.html', context=context, )


def idea_overview_detail(request, category_name, idea_id, detailed_view):
    current_idea = get_object_or_404(OnlineIdea, id=idea_id)
    # This idea id is used when saving the idea to a PlanCategoryOnlineIdea Object
    request.session['current_idea'] = current_idea.pk
    request.session['current_category']= category_name

    note_form = NotesForm()
    try:
        pcoi_obj = PlanCategoryOnlineIdea.objects.get(
            plan=Plan.objects.get(pk=request.session['current_user_plan']),
            category=Category.objects.get(category_url=request.session['current_category']),
            idea=OnlineIdea.objects.get(pk=request.session['current_idea']),

        )
        note_form = NotesForm(initial={'note_content': pcoi_obj.notes})
    except:
        pcoi_obj = None

    context = {
        'idea': current_idea,
        'note_form': note_form,
        'current_category': category_name,
        'plan_form': PlanForm()
    }

    # handles all logic when user adds idea or/and note from the idea_detail page
    if request.method == "POST":
        # checks if user has already created a plan
        if not has_plan(request):
            return redirect(request.META.get('HTTP_REFERER'))
        note_form = NotesForm(request.POST)
        if note_form.is_valid():
            if pcoi_obj is None:
                pcoi_obj = PlanCategoryOnlineIdea.objects.create(
                    plan=Plan.objects.get(pk=request.session['current_user_plan']),
                    category=Category.objects.get(category_url=request.session['current_category']),
                    idea=OnlineIdea.objects.get(pk=request.session['current_idea']),

                )

            pcoi_obj.notes = note_form.cleaned_data['note_content']
            pcoi_obj.save()

        return redirect('show_block', request.session['current_category'], request.session['current_next_page'])

    # manages get request
    if detailed_view == 'detailed_view':

        return render(request, 'plan/idea_detail.html', context=context)
    else:
        return render(request, 'plan/idea_overview.html', context=context)


@login_required
def checklist(request):
    if request.session['current_user_plan'] is not None:
        current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])
        c_s, c_d = context_summary(request.user, current_user_plan)
        context = {
            'context_summary': c_s,
            'category_done_summary': c_d,
            'current_plan':current_user_plan,
            'plan_form': PlanForm()
        }
        if 'crate_pdf' in request.GET:
            context.update({'category_objects': Category.objects.values_list('category_name', 'category_url',
                                                                             'next_page')})




            pdf = render_pdf('plan/checklist_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

            #return render(request, 'plan/checklist_pdf.html', context=context)
        else:

            return render(request, 'plan/checklist.html', context=context)
    else:
        messages.add_message(request, messages.INFO, 'First add a plan to be able to see the checklist page')
        return redirect('show_block', request.session['current_category'], request.session['current_next_page'])


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
                request.session['current_user_plan_name'] = new_plan.plan_name


        except IntegrityError:
            messages.add_message(request, messages.INFO, 'This plan already exists')

    # When user logs in, is prompted to create a course/plan by being redirected to a form, this if statement handles
    # it.
    if start_add == 'get_started':
        if request.method == "POST":
            plan_to_database()

            return redirect('show_block', 'human_touch', 'teaching_material')

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
    # checks if user has already created a plan
    if not has_plan(request):
        return redirect(request.META.get('HTTP_REFERER'))

    current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])

    request.session['current_idea'] = request.GET.get('idea_id') or request.session['current_idea']
    # If there's no plan in the request.session['current_user_plan'] dictionary; grab the plan name from the DOM
    # request.session['current_user_plan'] = request.session['current_user_plan'] or request.GET.get('plan_name_dom')

    # If the system lost track of the current idea or category e.g., the server crashed; these are extracted from the
    # current URL
    # if GLOBAL_CONTEXT['current_idea'] is None:
    #     GLOBAL_CONTEXT['current_idea'] = request.META.get('HTTP_REFERER').split('/')[4]
    # elif GLOBAL_CONTEXT['current_category'] is None:
    #     GLOBAL_CONTEXT['current_category'] = request.META.get('HTTP_REFERER').split('/')[3]

    if request.GET.get('delete_idea'):
        # Delete object
        PlanCategoryOnlineIdea.objects.filter(
            Q(plan__user=request.user) & Q(plan__pk=request.session['current_user_plan']) & Q(
                category__category_url=request.session['current_category']) & Q(
                idea__pk=request.session['current_idea']))[0].delete()
        # todo add to sessions as this is also computed in select_plan view
        # categories for which user has already selected at least one idea
        category_ready = category_done(current_user_plan)
        json_dic = {
            'category_ready': list(category_ready),
            "category_id": request.session['current_category'],
            'plan_id': request.session['current_user_plan']
        }
        return JsonResponse(json_dic)


    else:
        # prevents user from saving the same ideas twice for the same course plan.


        try:
            PlanCategoryOnlineIdea.objects.create(
                plan=Plan.objects.get(pk=request.session['current_user_plan']),
                category=Category.objects.get(category_url=request.session['current_category']),
                idea=OnlineIdea.objects.get(pk=request.session['current_idea']),

            )


        except IntegrityError:

            messages.add_message(request, messages.INFO, 'This idea has been already added to you course plan')
            return redirect(request.META.get('HTTP_REFERER'))

    json_dic = {
        "category_id": request.session['current_category'],
        'plan_id': request.session['current_user_plan']
    }
    # if user has either deleted or added an idea using the checkboxes on the blocks/category page
    if is_ajax(request):
        return JsonResponse(json_dic)
    else:
        # if user has selected and idea using the buttons provided by both the overview or detail idea page.
        return redirect('show_block', request.session['current_category'], request.session['current_next_page'])


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
    request.session['current_user_plan_name'] = current_user_plan.plan_name
    # categories for which user has already selected at least one idea
    category_ready = category_done(current_user_plan)

    response_dict = {
        'category_ready': list(category_ready),
        # this is the name that is shown on the top right (Name is changed dynamically through the DOM)
        'plan_name_ajax': request.session['current_user_plan_name'],
        # this is the id assigned to the div element that contains all blocks/categories on the sidebar
        'plan_id_response': request.GET.get('plan_id')
    }

    return JsonResponse(response_dict)


def update_selected_idea(request):
    """
    Updates the content of the block_content page such that when the user switches to a different course/plan using
    the side navigation bar, the ticked-off ideas reflect that of the current chosen plan/course
    """
    context = {'category': get_category(request.session['current_category']),
               'ideas_list': get_ideas(request.user, request.session['current_category'],
                                       request.session['current_user_plan']),
               'current_category': request.session['current_category']
               }

    return render(request, 'plan/update_ideas.html', context=context)

def delete_plan (request, plan_id):
    Plan.objects.get(pk=plan_id).delete()
    messages.add_message(request, messages.INFO, 'Your plan was deleted.')
    # if user deletes current plan (the plan she is working on)
    if str(plan_id) == request.session['current_user_plan']:
        p= Plan.objects.get_user_plans(request.user).last()
        request.session['current_user_plan'] =p.pk
        request.session['current_user_plan_name']= p.plan_name
        return redirect('show_block', 'human_touch', 'teaching_material')
    else:
        return redirect(request.META.get('HTTP_REFERER'))




# todo delete
def test_code(request):
    # current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])
    # c_s, c_d = context_summary(request.user, current_user_plan)
    # request_context = RequestContext (request)
    # category_obj =request_context.get('category_objects')
    #
    # context = {
    #     'context_summary': c_s,
    #     'category_done_summary': c_d,
    #     'current_plan': current_user_plan,
    #     'plan_form': PlanForm(),
    #     'category_objects': Category.objects.values_list('category_name', 'category_url', 'next_page')
    # }
    # pdf = render_to_pdf('plan/checklist_pdf.html',context)
    # return HttpResponse(pdf, content_type='application/pdf')
    # # return render(request,'plan/checklist_pdf.html', locals())
    return render(request,'plan/test_code.html', locals())