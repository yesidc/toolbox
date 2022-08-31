from tbcore.models import Plan

def user_plans (request):
    if request.user.is_authenticated:
        #TODO filter plan by users, here all plans are being shown

        #plans = Plan.objects.filter(user=request.user
        plans = Plan.objects.select_related('user').filter(user=request.user)
        return {'user_filter_plans':plans}
    else:
        return {}
