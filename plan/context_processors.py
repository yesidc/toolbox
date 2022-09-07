from tbcore.models import Plan

def user_plans (request):
    """
    Filters plans by user.
    """
    if request.user.is_authenticated:


        #plans = Plan.objects.filter(user=request.user
        plans = Plan.objects.select_related('user').filter(user=request.user)
        return {'user_filter_plans':plans}
    else:
        return {}


