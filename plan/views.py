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
        active_user_plan = 'button-state-plan-side-bar-' + slugify(request.session['current_user_plan_name'])
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



def idea_overview_detail(request, category_name, idea_id):
    """
    Implements all the logic related to showing a teaching tool detailed view.
    """

    current_idea = get_object_or_404(OnlineIdea, id=idea_id)
    # if the user created a note without login, the note content is cached in the session and loaded in the note form
    note_form = NotesForm()

    context = {
        'idea': current_idea,
        'note_form': note_form,
        'current_category': category_name,
        'plan_form': PlanForm()
    }

    if 'preserve_note' in request.GET:
        if 'note_content' in request.session:
            note_content = request.session['note_content']
            del request.session['note_content']
            note_form = NotesForm(initial={'note_content': note_content})
    else:
        if 'note_content' in request.session:
            del request.session['note_content']

    if 'current_user_plan' in request.session:

        active_user_plan = 'button-state-plan-side-bar-' + slugify(request.session['current_user_plan_name'])
        context.update({'active_user_plan': active_user_plan})
        pcoi_obj = PlanCategoryOnlineIdea.objects.pcoi_obj_exists(request.session['current_user_plan'], category_name,
                                                              idea_id)
        # loads current note giving the user the possibility to edit it.
        if pcoi_obj:
            note_form = NotesForm(initial={'note_content': pcoi_obj.notes})
    else:
        pcoi_obj = None




    # handles all logic when user adds/updates idea or/and note from the idea_detail page
    if request.method == "POST":
        # checks if user has already created a plan
        if not request.user.is_authenticated:
            # todo fix messages, it should be shown on login page

            # cache note content in session
            request.session['note_content'] = request.POST['note_content']

            messages.add_message(request, messages.INFO, 'First login to be able to save your notes')
            return redirect(f'/login/?category_name={category_name}&idea_id={idea_id}')
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
        messages.add_message(request, messages.INFO, f'Teaching Tip "{OnlineIdea.objects.get(pk=idea_id).idea_name}" was added to your course plan: "{request.session["current_user_plan_name"]}"')
        return redirect('show_block', category_name, Category.objects.get(category_url=category_name).next_page)

    # manages get request


    return render(request, 'plan/idea_detail.html', context=context)


@login_required
def checklist(request):
    """
    Creates a summary that comprises all the teaching tools selected by the user.
    """

    # if request.session['current_user_plan'] is not None:
    if 'current_user_plan' in request.session:
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
            'active_user_plan':'button-state-plan-side-bar-' + slugify(current_user_plan.plan_name), # used by localStorage to keep track of the active plan
            'plan_form': PlanForm()
        }


        if 'crate_pdf' in request.GET:
            context.update({'category_objects': Category.objects.values_list('category_name', 'category_url',
                                                                             'next_page')})

            pdf = render_pdf('plan/checklist_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        else:

            return render(request, 'plan/checklist.html', context=context)
    else:
        return redirect(request.META.get('HTTP_REFERER'))

# todo checklist page should be reload when user edits the plan title
def update_note_checklist(request):
    """
    Updates the note for a given teaching tool from the checklist page.
    """
    poci_obj = get_object_or_404(PlanCategoryOnlineIdea, pk=request.POST['pcoiId'])
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            poci_obj.notes = form.cleaned_data['note_content']
            poci_obj.save()

        # poci_obj.notes = request.POST['note_content']
        # poci_obj.save()
            return JsonResponse({'success': True,
                                 'note_content': poci_obj.notes,})
        else:
            messages.add_message(request, messages.INFO, 'Something went wrong, please try again')
            return JsonResponse({'success': False})
    else:
        return render(request, 'plan/checklist.html')

@login_required
def edit_plan_title(request):
    """
    Updates the title of a plan.
    """
    # todo while editing the collapsible should be closed

    if request.method == 'POST':
        plan_id = request.POST.get('planId')
        plan = Plan.objects.get(id=plan_id)
        previous_name = slugify(plan.plan_name)
        form = PlanForm(request.POST)
        if form.is_valid():

            try:

                updated_plan_name = form.cleaned_data['plan_name']
                plan.plan_name = updated_plan_name
                plan.save()
                request.session['current_user_plan_name'] = updated_plan_name
                return JsonResponse({'success': True,
                                     'previous_name': previous_name,
                                     'updated_name': slugify(updated_plan_name)})
            except Plan.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Plan not found.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method or not an AJAX request.'})

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

            return redirect('show_block', 'human-touch', 'teaching-material')

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

# todo delete this function, it was used to handle the checkboxes on the building block page.
# @login_required
# def use_idea(request, save_note=None):
#     """
#     Saves or deletes ideas from an existing course plan when the user interacts with the checkboxes displayed on the
#     building block page.
#     """
#
#     # checks if user has already created a plan
#     if not has_plan(request):
#         return redirect(request.META.get('HTTP_REFERER'))
#
#     if 'current_user_plan' in request.session:
#         current_user_plan = Plan.objects.get(pk=request.session['current_user_plan'])
#     else:
#
#         return redirect(request.META.get('HTTP_REFERER'))
#
#
#     current_idea = request.GET.get('idea_id')
#     current_category = request.GET.get('current_category')
#
#     if request.GET.get('delete_idea'):
#         # Delete object
#         obj_delete = PlanCategoryOnlineIdea.objects.get_or_none(request.user, request.session['current_user_plan'],
#                                                                 current_category, current_idea)
#         if obj_delete:
#             obj_delete.delete()
#
#
#         # categories for which user has already selected at least one idea
#         category_ready = category_done(current_user_plan)
#         json_dic = {
#             'category_ready': list(category_ready),
#             "category_id": current_category,
#             'plan_id': request.session['current_user_plan']
#         }
#         return JsonResponse(json_dic)
#
#
#
#     else:
#
#         save_pcoi(request, request.session['current_user_plan'], current_category, current_idea)
#
#     json_dic = {
#         "category_id": current_category,
#         'plan_id': request.session['current_user_plan']
#     }
#     # if user has either deleted or added an idea using the checkboxes on the blocks/category page
#     if is_ajax(request):
#         return JsonResponse(json_dic)
#     # else:
#     #     # if user has selected and idea using the buttons provided by both the overview or detail idea page.
#     #     return redirect('show_block', request.session['current_category'], request.session['current_next_page'])


@login_required()
def delete_pcoi_checklist(request):
    """
    Manages all related to deleting PlanCategoryOnlineIdea objects when registration interact with the checklist page
    """
    pcoi_delete = PlanCategoryOnlineIdea.objects.get(pk=request.GET.get('pcoi_id'))
    pcoi_category = pcoi_delete.category.category_name
    pcoi_delete.delete()
    remaining_ideas = PlanCategoryOnlineIdea.objects.select_related('plan__user', 'category').filter(
        Q(plan__user=request.user)& Q(plan=request.session['current_user_plan'])&Q(category__category_name=pcoi_category)).count()
    if remaining_ideas >0:
        delete_block= False

    else:
        delete_block = True


    # PlanCategoryOnlineIdea.objects.get(pk=request.GET.get('pcoi_id')).delete()
    return JsonResponse({'delete_block':delete_block, 'pcoi_category': slugify(pcoi_category)}, status=200)


@login_required()
def select_plan(request):
    """
    Triggered when user chooses to work on a different plan. User can switch to a
    different plan using the navigation bar on the left.
    """
    # update current_user_plan stored in sessions.
    request.session['current_user_plan'] = int(request.GET.get('plan_id'))

    current_user_plan = Plan.objects.get(pk=request.GET.get('plan_id'))
    request.session['current_user_plan_name'] = current_user_plan.plan_name
    # categories for which user has already selected at least one idea
    category_ready = category_done(current_user_plan)
    # category_idea_checklist is a list that contains a tuple whose items are the name of the building block and a list of all ideas
    # category_done_summary is a set that contains the name of the building block
    category_idea_checklist,category_done_summary = context_summary(request.user,
                                                                    Plan.objects.get(pk=request.session['current_user_plan']),
                                                                    checklist=False)
    response_dict = {
        #'category_ready': list(category_ready),
        'category_ready':category_idea_checklist,
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

    if plan_id == request.session['current_user_plan']:
        p = Plan.objects.get_user_plans(request.user).last()

        if p is not None:
            request.session['current_user_plan'] = p.pk
            request.session['current_user_plan_name'] = p.plan_name
        return redirect('show_block', 'human-touch', 'teaching-material')
    else:

        return redirect(request.META.get('HTTP_REFERER'))


