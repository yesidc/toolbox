from django.contrib.auth.models import User
from tbcore.models import *

def create_random_data (n):
    """
    creates n number of random users
    """
    for i in range(n):
        # create random users
        user = User.objects.create_user('tluser'+str(i), f'email{str(i)}@uni.com', '123'+str(i))

        Plan.objects.bulk_create([
            Plan(user=user, plan_name='tl' + str(i)),
            Plan(user=user, plan_name='tl'+str(i)+'test')
        ])
