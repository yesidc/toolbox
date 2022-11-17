from django.db import models
from django.contrib.auth.models import User
import json5
from tbcore.utils.fields import idea_fields, category_fields
from tbcore.utils.base import Json5ParseException


# Create your models here


class PlanCategoryOnlineIdeaManager(models.Manager):
    def get_pcoi(self, current_user, current_plan):
        """
        Returns all PlanCategoryOnlineIdea (pcoi) objects related to current user and current plan
        Args:
            current_user: current logged-in user
            current_plan: current active plan/course
        """
        return self.get_queryset().select_related('plan', 'idea').filter(plan__user=current_user, plan=current_plan)


class PlanManager(models.Manager):

    def get_user_plans(self, current_user):
        """
           Filters plan by user
           Args:
               current_user: current logged user
           """
        return self.get_queryset().select_related('user').filter(user=current_user)


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)  # usually something like course title
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
        c = self.plan_category_onlide_idea_plan.select_related('category')
        if mode == 'url':
            # iterates over the PlanCategoryOnlineIdea instances
            for p in c:
                # category url (as specified in the database)
                plan_category.add(p.category.category_url)
        else:
            for p in c:
                # category url (as specified in the database)
                plan_category.add(p.category.category_name)
        return plan_category


class Category(models.Model):
    category_name = models.CharField(
        max_length=100)  # there are a total of 8 categories: human touch, organization etc.
    category_id = models.SlugField(max_length=70, unique=True)  # internal id
    short_description = models.TextField()
    titles_accordion = models.TextField(null=True)  # accordion info
    content_accordion = models.TextField(null=True)  # requirements --> added to the accordion (building block page)
    references = models.TextField(null=True)
    category_url = models.CharField(max_length=50)
    next_page = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ('category_id',)

    @classmethod
    def create_from_json5(cls, data_json5):
        """
                Extracts idea's information from a json5 file and saves it to the database
                """

        category = json5.loads(data_json5)

        try:
            next_page = category["next_page"]
        except:
            category['next_page'] = None


        try:
            obj = Category.objects.get(category_id=category['category_id'])
            for key, value in category.items():
                setattr(obj, key, value)
            obj.save()
        except Category.DoesNotExist:
            obj = Category(**category)
            obj.save()




class OnlineIdea(models.Model):
    idea_name = models.CharField(max_length=200)
    idea_id = models.SlugField(max_length=70, unique=True)  # internal id
    brief_description = models.TextField()  # used for checklist on the building block page
    technology = models.TextField()
    implementation_steps = models.TextField(null=True)
    teacher_effort = models.TextField()
    recommendations = models.TextField()
    supplementary_material = models.TextField(null=True)
    testimony = models.TextField(null=True)
    use_cases = models.TextField(null=True)
    references = models.TextField(null=True)
    reusable = models.TextField(null=True)
    task_complexity = models.CharField(max_length=3, null=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.idea_name

    @staticmethod
    def add_category_to_idea(obj, idea_category):
        if isinstance(idea_category, list):
            for c in idea_category:
                try:
                    obj.category.add(Category.objects.get(category_url=c))
                except Category.DoesNotExist:
                    print(f'this category does not exist: {c}')
        else:
            try:
                obj.category.add(Category.objects.get(category_url=idea_category))
            except Category.DoesNotExist:
                print(f'this category does not exist: {idea_category}')

    @classmethod
    def create_from_json5(cls, data_json5):
        """
        Extracts idea's information from a json5 file and saves it to the database
        """

        idea = json5.loads(data_json5)


        try:
            obj = OnlineIdea.objects.get(idea_id=idea['idea_id'])
            for key, value in idea.items():
                if key != 'category':
                    setattr(obj, key, value)
            obj.save()
            OnlineIdea.add_category_to_idea(obj, idea['category'])
        except OnlineIdea.DoesNotExist:
            idea_ = idea.pop('category', None)
            obj = OnlineIdea(**idea)
            obj.save()

            OnlineIdea.add_category_to_idea(obj, idea_)




class PlanCategoryOnlineIdea(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_category_onlide_idea_plan')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plan_category_onlide_idea_category')
    idea = models.ForeignKey(OnlineIdea, on_delete=models.CASCADE, null=True,
                             related_name='plan_category_onlide_idea_i')
    notes = models.TextField(max_length=500, null=True)  # todo delete the null this is mandatory
    objects = PlanCategoryOnlineIdeaManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['plan', 'category', 'idea'], name='plancategoryonlineidea_constraint')
        ]

    @staticmethod
    def check_json5(data_json5, mode):
        """
        Check if a JSON5 representation of an idea or category is valid.
        Args:
            data_json5: Json5 file containing either an online idea or category data.
            mode: OnlineIdea or Category fields.
        """

        try:
            d_json5 = json5.loads(data_json5)
        except ValueError as err:
            raise Json5ParseException("Error in JSON5 code Error message: '{}'".format(err))

        if not isinstance(d_json5, dict):
            raise Json5ParseException("Data  must be a dictionary.")

        json5_fields = idea_fields() if mode == 'ideas' else category_fields()

        # Checks
        for field in json5_fields:
            # these fields are not mandatory
            if field not in ['testimony', 'next_page', 'references', 'supplementary_material', 'reusable', 'implementation_steps',
                             'use_cases', 'titles_accordion', 'content_accordion']:
                if field not in d_json5:
                    raise Json5ParseException('Field "{}" is missing'.format(field))
                if not d_json5[field]:
                    raise Json5ParseException('Field "{}" is empty'.format(field))
        return True

