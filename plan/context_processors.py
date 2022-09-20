from tbcore.models import Plan, Category

def user_plans (request):
    """
    Filters plans by user.
    """
    if request.user.is_authenticated:



        plans = Plan.objects.select_related('user').filter(user=request.user)
        return {'user_filter_plans':plans}
    else:
        return {}


def category_obj (request):
    """
    Returns list of tuples (category_name, category_url)
    """
    return {'category_objects': Category.objects.values_list('category_name','category_url','next_page')}