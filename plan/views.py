from django.shortcuts import render
from tbcore.models import *
# Create your views here.




def human_touch (request):
    category_human_touch = Category.objects.get(category_name='Human Touch')

    context ={'category':category_human_touch}
    return render(request,'plan/block_content.html', context=context)

def teaching_material (request):
    category_teaching_material = Category.objects.get(category_name='Teaching Material')

    context = {'category': category_teaching_material}
    return render(request,'plan/block_content.html', context=context)

def organization (request):
    category_organization = Category.objects.get(category_name='Organization')

    context = {'category': category_organization}
    return render(request,'plan/block_content.html', context=context)

def assignment (request):
    category_assignmet = Category.objects.get(category_name='Assignments')

    context = {'category': category_assignmet}
    return render(request,'plan/block_content.html', context=context)

def discussion (request):
    category_discussion = Category.objects.get(category_name='Discussion')

    context = {'category': category_discussion}
    return render(request,'plan/block_content.html', context=context)

def student_engagement (request):
    category_student_engagement = Category.objects.get(category_name='Student Engagement')

    context = {'category': category_student_engagement}
    return render(request,'plan/block_content.html', context=context)

def assessment (request):
    category_assessment = Category.objects.get(category_name='Assessment')

    context = {'category': category_assessment}
    return render(request,'plan/block_content.html', context=context)

def rules_regulations (request):
    category_rules_regulations = Category.objects.get(category_name='Rules & Regulations')

    context = {'category': category_rules_regulations}
    return render(request,'plan/block_content.html', context=context)



