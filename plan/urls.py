from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('category/<str:category_url>/<str:next_page>/', views.show_block, name='show_block'),
    # path('human_touch/', views.human_touch, name='human_touch'),

    path('<str:category_name>/<int:idea_id>/<str:detailed_view>/', views.idea_overview_detail,
         name='idea_overview_detail'),
    path('use_idea/', views.use_idea, name='use_idea'),
    path('create_plan/<str:start_add>/', views.create_plan, name='create_plan'),
    path('select_plan/', views.select_plan, name='select_plan'),
    path('update_selected_idea/', views.update_selected_idea, name='update_selected_idea'),
    path('delete_pcoi_checklist/', views.delete_pcoi_checklist, name='delete_pcoi_checklist'),

    path('checklist/', views.checklist, name='checklist'),
    path('delete_plan/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('test_code/', views.test_code, name='test_code'), #todo delete

]
