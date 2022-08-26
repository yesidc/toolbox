from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('human_touch/', views.human_touch, name='human_touch'),
    path('teaching_material/', views.teaching_material, name='teaching_material'),
    path('organization/', views.organization, name='organization'),
    path('assignment/', views.assignment, name='assignment'),
    path('student_engagement/', views.student_engagement, name='student_engagement'),
    path('discussion/', views.discussion, name='discussion'),
    path('assessment/', views.assessment, name='assessment'),
    path('rules_regulations/', views.rules_regulations, name='rules_regulations'),
   path('<str:category_name>/<int:idea_id>/<str:detailed_view>/', views.idea_overview_detail, name='idea_overview_detail'),
    path('save_idea/', views.use_idea, name='use_idea'),
    path('create_plan/<str:start_add>/', views.create_plan, name='create_plan'),
    path('select_plan/<int:plan_id>/', views.select_plan, name='select_plan'),

   path('summary/', views.summary, name='summary'),

]
