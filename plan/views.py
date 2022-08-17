from django.shortcuts import render, get_object_or_404
from tbcore.models import *

# Create your views here.


IDEA_PROPERTIES = ('idea_name', 'brief_description', 'examples_application',
                   'tool', 'implementation_steps', 'teacher_effort',
                   'recommendations', 'supplementary_material', 'reusable',
                   'testimony', 'references')


# todo use get_object_or_404() function with all the category_block_name variable

def human_touch(request):
    category_human_touch = CategoryOnlineIdea.objects.get(category__category_name='Human Touch')

    context = {'category': category_human_touch,
               'next_page': 'teaching_material',
               'name_next_page': 'Teaching Material'}
    return render(request, 'plan/block_content.html', context=context)


def teaching_material(request):
    category_teaching_material = CategoryOnlineIdea.objects.get(category__category_name='Teaching Material')

    context = {'category': category_teaching_material,
               'next_page': 'organization',
               'name_next_page': 'Organization'}
    return render(request, 'plan/block_content.html', context=context)


def organization(request):
    category_organization = CategoryOnlineIdea.objects.get(category__category_name='Organization')

    context = {'category': category_organization,
               'next_page': 'assignment',
               'name_next_page': 'Assignment'}
    return render(request, 'plan/block_content.html', context=context)


def assignment(request):
    category_assignmet = CategoryOnlineIdea.objects.get(category__category_name='Assignments')

    context = {'category': category_assignmet,
               'next_page': 'discussion',
               'name_next_page': 'Discussion'}
    return render(request, 'plan/block_content.html', context=context)


def discussion(request):
    category_discussion = CategoryOnlineIdea.objects.get(category__category_name='Discussion')

    context = {'category': category_discussion,
               'next_page': 'student_engagement',
               'name_next_page': 'Student Engagement'}
    return render(request, 'plan/block_content.html', context=context)


def student_engagement(request):
    category_student_engagement = CategoryOnlineIdea.objects.get(category__category_name='Student Engagement')

    context = {'category': category_student_engagement,
               'next_page': 'assessment',
               'name_next_page': 'Assessment'}
    return render(request, 'plan/block_content.html', context=context)


def assessment(request):
    category_assessment = CategoryOnlineIdea.objects.get(category__category_name='Assessment')

    context = {'category': category_assessment,
               'next_page': 'rules_regulations',
               'name_next_page': 'Rules & Regulations'}
    return render(request, 'plan/block_content.html', context=context)


def rules_regulations(request):
    category_rules_regulations = CategoryOnlineIdea.objects.get(category__category_name='Rules & Regulations')

    context = {'category': category_rules_regulations}
    return render(request, 'plan/block_content.html', context=context)


def idea_overview_detail(request, idea_id, detailed_view):
    idea = get_object_or_404(OnlineIdea, id=idea_id)
    context = {
        'idea': idea,

    }
    if detailed_view == 'detailed_view':
        return render(request, 'plan/idea_detail.html', context=context)
    else:
        return render(request, 'plan/idea_overview.html', context=context)


# def idea_detail(request):
#     return render(request, 'plan/idea_detail.html')


def summary(request):
    return render(request, 'plan/summary.html')
