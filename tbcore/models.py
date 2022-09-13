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
        return self.get_queryset().select_related('plan').filter(plan__user=current_user,plan=current_plan)


class Plan (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #todo should be unique, there should not be more than one plan with the same name.
    plan_name = models.CharField(max_length=100)  #usually something like course title

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
        if mode=='url':
            # iterates over the PlanCategoryOnlineIdea instances
            for p in self.plan_category_onlide_idea_plan.all():
                # category url (as specified in the database)
                plan_category.add(p.category.category_url)
        else:
            for p in self.plan_category_onlide_idea_plan.all():
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
    notes = models.ForeignKey(Notes, related_name='note_plan',on_delete= models.CASCADE,
                              null=True)  # todo delete the null this is mandatory
    objects=PlanCategoryOnlineIdeaManager()

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['plan','category','idea'], name='plancategoryonlineidea_constraint')
        ]


