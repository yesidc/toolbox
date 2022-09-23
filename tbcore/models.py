from django.db import models
from django.contrib.auth.models import User
# Create your models here




class PlanCategoryOnlineIdeaManager (models.Manager):
    def get_pcoi(self, current_user, current_plan):
        """
        Returns all PlanCategoryOnlineIdea (pcoi) objects related to current user and current plan
        Args:
            current_user: current logged-in user
            current_plan: current active plan/course
        """
        return self.get_queryset().select_related('plan','idea').filter(plan__user=current_user,plan=current_plan)


class PlanManager(models.Manager):

    def get_user_plans (self, current_user):
        """
           Filters plan by user
           Args:
               current_user: current logged user
           """
        return self.get_queryset().select_related('user').filter(user=current_user)

class Plan (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)  #usually something like course title
    objects = PlanManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['plan_name', 'user'], name='plan_constraint')
        ]

    def __str__(self):
        return self.plan_name

    def category_done(self, mode='url'):
        """
        Returns a set of categories (urls, as specified in the database) for which a user has already selected at least one idea.
        Args:
            mode: if it is url, returns set of category urls, otherwise; returns the name of the category
        """
        # categories/blocks for which the user has already selected an idea
        plan_category = set()
        c=self.plan_category_onlide_idea_plan.select_related('category')
        if mode=='url':
            # iterates over the PlanCategoryOnlineIdea instances
            for p in c:
                # category url (as specified in the database)
                plan_category.add(p.category.category_url)
        else:
            for p in c:
                # category url (as specified in the database)
                plan_category.add(p.category.category_name)
        return plan_category



class Category (models.Model):
    category_name = models.CharField(max_length=100) # there are a total of 8 categories: hallway chatter, organization etc.
    short_description = models.TextField()
    further_information = models.TextField(null=True)
    reasons = models.TextField()
    references = models.TextField(null=True)
    category_url= models.CharField(max_length=50)
    next_page = models.CharField(max_length=100, null=True)


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


    def __str__(self):
        return self.idea_name




class CategoryOnlineIdea (models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    online_idea = models.ManyToManyField(OnlineIdea) #todo implement related name
    # display = models.BooleanField()



class PlanCategoryOnlineIdea (models.Model):
    plan = models.ForeignKey(Plan, on_delete= models.CASCADE,  related_name = 'plan_category_onlide_idea_plan')
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name= 'plan_category_onlide_idea_category')
    idea = models.ForeignKey (OnlineIdea, on_delete= models.CASCADE, null= True,related_name= 'plan_category_onlide_idea_i')
    notes = models.TextField(max_length=500,null=True)  # todo delete the null this is mandatory
    objects=PlanCategoryOnlineIdeaManager()

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['plan','category','idea'], name='plancategoryonlineidea_constraint')
        ]


