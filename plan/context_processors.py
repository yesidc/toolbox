from tbcore.models import Plan, Category

def user_plans (request):
    """
    Filters plans by user.
    """
    if request.user.is_authenticated:



        #plans = Plan.objects.select_related('user').filter(user=request.user)
        return {'user_filter_plans':Plan.objects.get_user_plans(request.user)}
    else:
        return {}


def category_obj (request):
    """
    Returns list of tuples (category_name, category_url, next_page)
    """
    category_objects= Category.objects.values_list('category_name','category_url','next_page')
    # This list is eventually used by menu_bar.js to active links on top nav bar.
    #category_urls = {c_url:c_url for c_name,c_url,_ in category_objects}
    category_urls = [c_url for _,c_url,_ in category_objects]

    return {'category_objects': category_objects, 'category_urls': category_urls}