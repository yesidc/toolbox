from django.db import models
from django.contrib.auth.models import User
# Create your models here






class Plan (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)  #usually something like course title

    def __str__(self):
        return self.plan_name

class Category (models.Model):
    category_name = models.CharField(max_length=100) # there are a total of 8 categories: hallway chatter, organization etc.
    short_description = models.TextField()
    further_information = models.TextField(null=True)
    reasons = models.TextField()
    references = models.TextField(null=True)


    def __str__(self):
        return self.category_name

class OnlineIdea (models.Model):
    idea_name = models.CharField (max_length= 200)
    brief_description = models.TextField() # used for checklist on the building block page
    examples_application = models.TextField(null=True)
    tool = models.TextField(null=True)
    implementation_steps = models.TextField(null=True)
    teacher_effort = models.TextField()
    recommendations = models.TextField()
    supplementary_material = models.TextField()
    reusable = models.TextField(null=True)
    testimony = models.TextField(null=True)
    references = models.TextField( null=True)
    #todo add how I plan to implement this idea. This field is not mandatory

    def __str__(self):
        return self.idea_name


# class CategoryOnlineIdea1 (models.Model):
#     #todo if category is deleted this object 'CategoryOnlineIdea' should be delted as well
#     category = models.ManyToManyField(Category) #todo here you need something like on_delete
#     online_idea = models.ForeignKey(OnlineIdea, on_delete = models.CASCADE)  #todo implement related name
#     display = models.BooleanField()


class CategoryOnlineIdea (models.Model):
    #todo if category is deleted this object 'CategoryOnlineIdea' should be delted as well
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    online_idea = models.ManyToManyField(OnlineIdea) #todo implement related name
    # display = models.BooleanField()

#todo needs a user field as a note also belongs to a single user, although a Plan object already belongs to a User, so maybe this is not needed.
# todo retrieve all the notes that belong a user and then all the notes that belong to a particular idea.
class Notes (models.Model):
    idea_note = models.TextField(null=True) #todo delete null. we do not wat user to submit empy object
    online_idea = models.ForeignKey(OnlineIdea, on_delete=models.CASCADE, related_name='note_online_idea')



#todo do we want to delete this object if for example a category is deleted?

class PlanCategoryOnlineIdea (models.Model):
    plan = models.ForeignKey(Plan, on_delete= models.CASCADE,  related_name = 'plan_category_onlide_idea_plan')
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'plan_category_onlide_idea_category')
    idea = models.ForeignKey (OnlineIdea, on_delete= models.CASCADE, null= True,related_name= 'plan_category_onlide_idea_i')
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='note_plan',
                             null=True)  # todo delete the null this is mandatory


