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
    description = models.TextField()
    short_description = models.TextField() # used for checklist on the building block page
    implementation_steps = models.TextField()
    teacher_effort = models.TextField()
    recommendations = models.TextField()
    supplementary_material = models.TextField()
    examples_application = models.TextField()
    testimony = models.TextField()
    references = models.TextField()
    #todo add how I plan to implement this idea. This field is not mandatory

    def __str__(self):
        return self.idea_name


class CategoryOnlineIdea (models.Model):
    #todo if category is deleted this object 'CategoryOnlineIdea' should be delted as well
    category = models.ManyToManyField(Category) #todo here you need something like on_delete
    online_idea = models.ForeignKey(OnlineIdea, on_delete = models.CASCADE)
    display = models.BooleanField()



class PlanCategoryOnlineIdea (models.Model):
    plan = models.ForeignKey(Plan, on_delete= models.CASCADE,  related_name = 'plan_category_onlide_idea_plan')
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'plan_category_onlide_idea_category')
    idea = models.ForeignKey (OnlineIdea, on_delete= models.CASCADE, null= True,related_name= 'plan_category_onlide_idea_i')
