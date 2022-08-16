from django.shortcuts import render
from tbcore.models import *
# Create your views here.


#todo use get_object_or_404() function

def human_touch (request):
    category_human_touch = Category.objects.get(category_name='Human Touch')

    context ={'category':category_human_touch,
              'next_page':'teaching_material',
              'name_next_page': 'Teaching Material'}
    return render(request,'plan/block_content.html', context=context)

def teaching_material (request):
    category_teaching_material = Category.objects.get(category_name='Teaching Material')

    context = {'category': category_teaching_material,
               'next_page': 'organization',
               'name_next_page': 'Organization'}
    return render(request,'plan/block_content.html', context=context)

def organization (request):
    category_organization = Category.objects.get(category_name='Organization')

    context = {'category': category_organization,
               'next_page':'assignment',
               'name_next_page': 'Assignment'}
    return render(request,'plan/block_content.html', context=context)

def assignment (request):
    category_assignmet = Category.objects.get(category_name='Assignments')

    context = {'category': category_assignmet,
               'next_page':'discussion',
               'name_next_page': 'Discussion'}
    return render(request,'plan/block_content.html', context=context)

def discussion (request):
    category_discussion = Category.objects.get(category_name='Discussion')

    context = {'category': category_discussion,
               'next_page': 'student_engagement',
               'name_next_page':'Student Engagement'}
    return render(request,'plan/block_content.html', context=context)

def student_engagement (request):
    category_student_engagement = Category.objects.get(category_name='Student Engagement')

    context = {'category': category_student_engagement,
               'next_page': 'assessment',
               'name_next_page':'Assessment'}
    return render(request,'plan/block_content.html', context=context)

def assessment (request):
    category_assessment = Category.objects.get(category_name='Assessment')

    context = {'category': category_assessment,
               'next_page':'rules_regulations',
               'name_next_page': 'Rules & Regulations'}
    return render(request,'plan/block_content.html', context=context)

def rules_regulations (request):
    category_rules_regulations = Category.objects.get(category_name='Rules & Regulations')

    context = {'category': category_rules_regulations}
    return render(request,'plan/block_content.html', context=context)

def idea_overview (request):
    return render (request,'plan/idea_overview.html')

def idea_detail (request):
    return render (request,'plan/idea_detail.html')

def summary (request):
    return render (request,'plan/summary.html')



