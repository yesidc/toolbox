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
    description = models.TextField()
    def __str__(self):
        return self.category_name

class OnlineIdea (models.Model):
    idea_name = models.CharField (max_length= 200)
    description = models.TextField()
    short_description = models.CharField(max_length= 200) # used for checklist

    def __str__(self):
        return self.idea_name


class CategoryOnlineIdea (models.Model):
    category = models.ManyToManyField(Category)
    online_idea = models.ForeignKey(OnlineIdea, on_delete = models.CASCADE)
    display = models.BooleanField()



class PlanCategoryOnlineIdea (models.Model):
    plan = models.ForeignKey(Plan, on_delete= models.CASCADE,  related_name = 'plan_category_onlide_idea_plan')
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'plan_category_onlide_idea_category')
    idea = models.ForeignKey (OnlineIdea, on_delete= models.CASCADE, null= True,related_name= 'plan_category_onlide_idea_i')
