from django.contrib.auth.models import User
from tbcore.models import *

def create_random_data (n):
    """
    creates n number of random users
    """
    for i in range(n):
        # create random users
        User.objects.create_user('tl'+str(i), f'email{str(i)}@uni.com', '123'+str(i))
