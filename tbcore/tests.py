from django.test import TestCase

#Create your tests here.
# from random import randrange
# from tbcore.models import CategoryOnlineIdea

# if 'user_progress' not in request.session:
    
#     request.session['user_progress'] = {}
    
# coi_saved =[]
# for i in range (15):
#     coi_id = randrange(1,27)
#     if coi_id in coi_saved:
#         continue
#     coi = CategoryOnlineIdea.objects.get(pk=coi_id)
#     category_name_query = coi.category.category_name
#     idea_name = coi.idea.idea_name
#     note = "Learning and teaching are more valuable, effective and worthwhile when we interact with others. Being in touch with others can often prevent students from dropping a course and keeps their interest in the topic. Particularly online students need opportunities to address topic"
#     task_complexity = coi.idea.task_complexity
#     request.session['user_progress'].update({str(coi_id): (category_name_query, idea_name, note, task_complexity)})
#     request.session.modified = True
#     print(coi)
            