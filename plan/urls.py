from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('category/<str:category_url>/<str:next_page>/', views.show_block, name='show_block'),
    # path('human_touch/', views.human_touch, name='human_touch'),

    path('<str:category_name>/teaching_tool/<int:idea_id>/', views.idea_overview_detail,
         name='idea_overview_detail'),
    #path('use_idea/', views.use_idea, name='use_idea'), todo delete, managed checkboxes on building block page
    path('create_plan/<str:start_add>/', views.create_plan, name='create_plan'),
    path('select_plan/', views.select_plan, name='select_plan'),
    path('delete_pcoi_checklist/', views.delete_pcoi_checklist, name='delete_pcoi_checklist'),

    path('checklist/', views.checklist, name='checklist'),
    path('delete_plan/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('update_note_checklist/', views.update_note_checklist, name='update_note_checklist'),




]
