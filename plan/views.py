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
from collections import namedtuple

Progress = namedtuple('Progress', ['category', 'idea_name', 'note', 'complexity'])






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
            context.update({'note_form': note_form})
    else:
        pcoi_obj = None


    if not request.user.is_authenticated:
        if 'user_progress' in request.session:
            idea_name = OnlineIdea.objects.get(pk=idea_id).idea_name
            category_name_session = Category.objects.get(category_url=category_name).category_name
            coi_instance_id = CategoryOnlineIdea.objects.get(category__category_name=category_name_session, idea__idea_name=idea_name).pk
            if str(coi_instance_id) in request.session['user_progress'].keys():
                note_form = NotesForm(initial={'note_content': request.session['user_progress'][str(coi_instance_id)][2]})
                context.update({'note_form': note_form})
        
        
        
        

    # handles all logic when user adds/updates idea or/and note from the idea_detail page
    if request.method == "POST":
        # TODO valid form should be checked before saving the note
        # checks if user has already created a plan
        if not request.user.is_authenticated:
            # todo fix messages, it should be shown on login page

            # cache note content in session
            # TODO CONTROL WHEN THE SESSION EXPIRE request.session.set_expiry(1800)  # Session will expire in 1800 seconds (30 minutes)
            # TODO request.session.set_expiry(0) session to expire when the user closes their browser --> settings.py SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            # namedtuple('Progress', ['category', 'idea_name', 'note', 'complexity'])
            # List whose elements are tuples with the following structure: [('teaching-material', [(...), (...), (...)]),]), ('human-touch', [...])]
            # where [idea_name, pcoi_instance_id,pcoi_instance_note,pcoi_instance_complexity]
            
            idea_name = OnlineIdea.objects.get(pk=idea_id).idea_name
            task_complexity = OnlineIdea.objects.get(pk=idea_id).task_complexity
            # uppercase the first letter of the category name
            category_name_query = category_name.replace('-', ' ').title()
            category_idea_obj = CategoryOnlineIdea.objects.filter(category__category_name=category_name_query, idea__idea_name=idea_name)   
            key_category_idea_obj = str(category_idea_obj[0].pk)
            
            if 'user_progress' not in request.session:
                request.session['user_progress'] = {}
             
            
            if key_category_idea_obj not in request.session['user_progress'].keys():
                request.session['user_progress'].update({key_category_idea_obj: (Progress(category_name_query, idea_name, request.POST['note_content'],
                                                                 task_complexity))})
                request.session.modified = True
            

            else:
                # update the note content
                request.session['user_progress'].update({key_category_idea_obj: (Progress(category_name, idea_name, request.POST['note_content'],
                                                                 task_complexity))})
            
                request.session.modified = True
            
            

            # messages.add_message(request, messages.INFO, 'First login to be able to save your notes')
            return redirect('idea_overview_detail', category_name, idea_id)
            # return redirect(f'/login/?category_name={category_name}&idea_id={idea_id}')
        
        
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
        # return redirect('show_block', category_name, Category.objects.get(category_url=category_name).next_page)
        return redirect(request.META.get('HTTP_REFERER'))

    # manages get request


    return render(request, 'plan/idea_detail.html', context=context)



def checklist(request):
    """
    Creates a summary that comprises all the teaching tools selected by the user.
    """


    if not request.user.is_authenticated:
          #List whose elements are tuples with the following structure: [('teaching-material', [(...), (...), (...)]),]), ('human-touch', [...])]
        # where [idea_name, pcoi_instance_id,pcoi_instance_note,pcoi_instance_complexity]
        # TODO pcoi_instance_id --> use to delete the pcoi object from checklist page. Also come up with a way to delete the object from the session
        # TODO pcoi_instance_id --> FIX, now it is just a placeholder
        # Progress = namedtuple('Progress', ['category', 'idea_name', 'note', 'complexity'])
        # category online idea object id
        from collections import defaultdict
        summary_dict = defaultdict(list)
        
        # [('teaching-material', [...])], where [('idea_name', coi_instance_id, note(str), complexity)]
        category_idea_checklist =[]
        category_done_summary = []
        # check if user has made any selection
        if 'user_progress' in request.session:
            for key, value in request.session['user_progress'].items():
                coi_instance_id = CategoryOnlineIdea.objects.get(pk=int(key))
                # value = ['category', 'idea_name', 'note', 'complexity']
                if value[0] not in summary_dict.keys():
                    summary_dict[value[0]].append((value[1], coi_instance_id.pk, value[2], value[3]))
                else:
                    summary_dict[value[0]].append((value[1], coi_instance_id.pk, value[2], value[3]))
                    
            for key, value in summary_dict.items():
                category_idea_checklist.append((key, value))
                category_done_summary.append(key)
            
            context = {
                    'context_summary': category_idea_checklist,
                    'category_done_summary': category_done_summary,
                    'plan_form': PlanForm()
                }
        else:
            messages.add_message(request, messages.INFO, 'First select a teaching tool to be able to see the checklist page')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
        if 'crate_pdf' in request.GET:
            context.update({'category_objects': Category.objects.values_list('category_name', 'category_url',
                                                                            'next_page')})

            pdf = render_pdf('plan/checklist_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

        else:

            return render(request, 'plan/checklist.html', context=context)
        
        
        
        
        
        # return render(request, 'plan/checklist.html', context=context)
    
    elif request.user.is_authenticated:
   
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
    else:
        messages.add_message(request, messages.INFO, 'First select a teaching tool to be able to see the checklist page')
        return redirect(request.META.get('HTTP_REFERER'))

# todo checklist page should be reload when user edits the plan title

def update_note_session_checklist(request):
    
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            # update note content in the session
            request.session['user_progress'][request.GET.get('coi_id')][2] = form.cleaned_data['note_content']
            request.session.modified = True
    
    return redirect('checklist')


@login_required
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



def checklist_cache(request):
    """
    Saves the notes and ideas selected by the user in the session.
    """
    #List whose elements are tuples with the following structure: [('teaching-material', [(...), (...), (...)]),]), ('human-touch', [...])]
    # where [idea_name, coi_instance_id,pcoi_instance_note,pcoi_instance_complexity]
    # TODO pcoi_instance_id --> use to delete the pcoi object from checklist page. Also come up with a way to delete the object from the session
    # TODO pcoi_instance_id --> FIX, now it is just a placeholder
    # Progress = namedtuple('Progress', ['category', 'idea_name', 'note', 'complexity'])
    # category online idea object id
    from collections import defaultdict
    summary_dict = defaultdict(list)
    
    
    category_idea_checklist =[]
    category_done_summary = []
    # check if user has made any selection
    if 'user_progress' in request.session:
        for key, value in request.session['user_progress'].items():
            coi_instance_id = CategoryOnlineIdea.objects.get(pk=int(key))
            # value = ['category', 'idea_name', 'note', 'complexity']
            if value[0] not in summary_dict.keys():
                summary_dict[value[0]].append((value[1], coi_instance_id.pk, value[2], value[3]))
            else:
                summary_dict[value[0]].append((value[1], coi_instance_id.pk, value[2], value[3]))
                
        for key, value in summary_dict.items():
            category_idea_checklist.append((key, value))
            category_done_summary.append(key)
        
        context = {
                'context_summary': category_idea_checklist,
                'category_done_summary': category_done_summary,
                'plan_form': PlanForm()
            }
    else:
        messages.add_message(request, messages.INFO, 'First select a teaching tool to be able to see the checklist page')
        return redirect(request.META.get('HTTP_REFERER'))
    
    

    
    return render(request, 'plan/checklist.html', context=context)
   

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



def delete_pcoi_checklist(request):
    """
    Manages all related to deleting PlanCategoryOnlineIdea objects when registration interact with the checklist page
    """
    # if the user is not logged in
    if not request.user.is_authenticated:
        # delete the object from the session
        del request.session['user_progress'][request.GET.get('pcoi_id')]
        request.session.modified = True
        return JsonResponse({'delete_block':False, 'session_data': True}, status=200)
    
    
    elif request.user.is_authenticated:
    
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
    else:
        messages.add_message(request, messages.INFO, 'First save a note to be able to delete it.')
        return redirect(request.META.get('HTTP_REFERER'))


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


