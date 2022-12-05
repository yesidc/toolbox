from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .helpers import category_done, is_ajax, context_summary, get_ideas, has_plan, save_pcoi
from tbcore.models import *
from .forms import NotesForm, PlanForm
from tbcore.utils.create_pdf import render_pdf
from django.core.exceptions import ObjectDoesNotExist


def show_block(request, category_url, next_page):
    """
    Manages the content for all building blocks/categories.

    """

    if 'current_user_plan' in request.session:
        ideas_list = get_ideas(request.user, category_url, request.session['current_user_plan'])
    else:
        ideas_list = None

    category = Category.objects.get(category_url=category_url)
    ideas = OnlineIdea.objects.prefetch_related('category').filter(
        category__category_url=category_url)  # these are the ideas displayed by default
    next_page = next_page
    current_category = category_url
    plan_form = PlanForm()  # User utilizes this form to create new plans/courses. Form available in all block pages.

    if 'mode' in request.GET:
        return render(request, 'plan/update_ideas.html', context=locals())
    else:
        return render(request, 'plan/block_content.html', context=locals())


def idea_overview_detail(request, category_name, idea_id, detailed_view):
    """
    Implements all the logic related to showing an overview or detailed view of a teaching tool.
    """
    current_idea = get_object_or_404(OnlineIdea, id=idea_id)

    note_form = NotesForm()
    if 'current_user_plan' in request.session:
        pcoi_obj = PlanCategoryOnlineIdea.objects.pcoi_obj_exists(request.session['current_user_plan'], category_name,
                                                              idea_id)
        # loads current note giving the user the possibility to edit it.
        if pcoi_obj:
            note_form = NotesForm(initial={'note_content': pcoi_obj.notes})
    else:
        pcoi_obj = None


    context = {
        'idea': current_idea,
        'note_form': note_form,
        'current_category': category_name,
        'plan_form': PlanForm()
    }

    # handles all logic when user adds/updates idea or/and note from the idea_detail page
    if request.method == "POST":
        # checks if user has already created a plan
        if not has_plan(request):
            return redirect(request.META.get('HTTP_REFERER'))
        note_form = NotesForm(request.POST)
        if note_form.is_valid():
            if pcoi_obj is None:
                pcoi_obj = PlanCategoryOnlineIdea.objects.create(
                    plan=Plan.objects.get(pk=request.session['current_user_plan']),
                    category=Category.objects.get(category_url=category_name),
                    idea=OnlineIdea.objects.get(pk=idea_id),

                )

            pcoi_obj.notes = note_form.cleaned_data['note_content']
            pcoi_obj.save()
        messages.add_message(request, messages.INFO, 'Idea successfully added to your plan')
        return redirect('show_block', category_name, Category.objects.get(category_url=category_name).next_page)

    # manages get request
    if detailed_view == 'detailed_view':

        return render(request, 'plan/idea_detail.html', context=context)
    else:
        return render(request, 'plan/idea_overview.html', context=context)


@login_required
def use_idea_overview(request, current_category, idea_id):
    """
    Saves idea to a current user plan when user interacts with the overview page.
    """
    # checks if user has already created a plan
    if not has_plan(request):
        return redirect(request.META.get('HTTP_REFERER'))

    saved = save_pcoi(request, request.session['current_user_plan'], current_category, idea_id)

    if saved:
        messages.add_message(request, messages.INFO, 'Idea successfully added to your plan')

        return redirect('show_block', current_category, Category.objects.get(category_url=current_category).next_page)
    else:
        messages.add_message(request, messages.INFO, 'This idea has been already added to you course plan')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def checklist(request):
    """
    Creates a summary that comprises all the teaching tools selected by the user.
    """

    if request.session['current_user_plan'] is not None:
        try:
            current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])
        except ObjectDoesNotExist:
            messages.add_message(request, messages.INFO, 'First add a plan to be able to see the checklist page')
            return redirect(request.META.get('HTTP_REFERER'))

        c_s, c_d = context_summary(request.user, current_user_plan)
        context = {
            'context_summary': c_s,
            'category_done_summary': c_d,
            'current_plan': current_user_plan,
            'plan_form': PlanForm()
        }
        if 'crate_pdf' in request.GET:
            context.update({'category_objects': Category.objects.values_list('category_name', 'category_url',
                                                                             'next_page')})

            pdf = render_pdf('plan/checklist_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        else:

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
        'form': form,
        'num_plans': Plan.objects.filter(user=request.user).count()

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

        return render(request, 'plan/start_course_login.html', context=context)
    elif start_add == 'add_new_plan':
        if request.method == "POST":
            plan_to_database()
            # user redirected to previous page
            return redirect(request.META.get('HTTP_REFERER'))





@login_required
def use_idea(request, save_note=None):
    """
    Saves or deletes ideas from an existing course plan when the user interacts with the checkboxes displayed on the building block page.
    """

    # checks if user has already created a plan
    if not has_plan(request):
        return redirect(request.META.get('HTTP_REFERER'))

    current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])

    current_idea = request.GET.get('idea_id')
    current_category = request.GET.get('current_category')

    if request.GET.get('delete_idea'):
        # Delete object
        obj_delete = PlanCategoryOnlineIdea.objects.get_or_none(request.user, request.session['current_user_plan'],
                                                                current_category, current_idea)
        if obj_delete:
            obj_delete.delete()

        # todo add to sessions as this is also computed in select_plan view
        # categories for which user has already selected at least one idea
        category_ready = category_done(current_user_plan)
        json_dic = {
            'category_ready': list(category_ready),
            "category_id": current_category,
            'plan_id': request.session['current_user_plan']
        }
        return JsonResponse(json_dic)



    else:

        save_pcoi(request, request.session['current_user_plan'], current_category, current_idea)

    json_dic = {
        "category_id": current_category,
        'plan_id': request.session['current_user_plan']
    }
    # if user has either deleted or added an idea using the checkboxes on the blocks/category page
    if is_ajax(request):
        return JsonResponse(json_dic)
    # else:
    #     # if user has selected and idea using the buttons provided by both the overview or detail idea page.
    #     return redirect('show_block', request.session['current_category'], request.session['current_next_page'])


@login_required()
def delete_pcoi_checklist(request):
    """
    Manages all related to deleting PlanCategoryOnlineIdea objects when users interact with the checklist page
    """

    PlanCategoryOnlineIdea.objects.get(pk=request.GET.get('pcoi_id')).delete()
    return JsonResponse({}, status=200)


@login_required()
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


@login_required()
def delete_plan(request, plan_id):
    """
    Deletes a course plan and redirects to the previous page.
    """
    Plan.objects.get(pk=plan_id).delete()
    messages.add_message(request, messages.INFO, 'Your course plan was deleted.')
    # if user deletes current plan (the plan she is working on)
    if str(plan_id) == request.session['current_user_plan']:
        p = Plan.objects.get_user_plans(request.user).last()

        if p is not None:
            request.session['current_user_plan'] = p.pk
            request.session['current_user_plan_name'] = p.plan_name
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

    return render(request, 'plan/test_code.html', locals())
