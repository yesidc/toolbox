from random import randrange
from lorem_text import lorem
from django.contrib.auth.models import User
from tbcore.models import *

def create_random_data (n):
    """
    creates n number of random registration along with their corresponding course plans. This function also populates each
    course plan with up to 27 ideas.
    """
    for i in range(n):
        # create random registration
        user = User.objects.create_user('tluser'+str(i), f'email{str(i)}@uni.com', '123'+str(i))

        plans = Plan.objects.bulk_create([
            Plan(user=user, plan_name='tl course test' + str(i)),
            Plan(user=user, plan_name='tl test'+str(i))
        ])
        num_ideas =randrange(1,27)
        for plan in plans:
            for n in range(num_ideas):
                word_count = randrange(10,70)
                # there are a total of 27 ideas
                idea_id = randrange(1,27)
                idea= OnlineIdea.objects.get(pk=idea_id)
                note= 'tluser'+str(i)+'----->'+idea.idea_name+'------>'+f"plan's name: {plan.plan_name}"+"----->"+lorem.words(word_count)
                try:
                    PlanCategoryOnlineIdea.objects.create(plan=plan, category=idea.category.all()[0], idea=idea, notes=note)
                except Exception as e:
                    print(e)

    print('data created successfully')






