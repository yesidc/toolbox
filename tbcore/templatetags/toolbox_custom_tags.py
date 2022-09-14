from django import template

register = template.Library()


@register.filter(name='add_hyphen')
def add_hyphen(value):
    """
    Replaces blank spaces with a hyphen
    """
    return value.replace(' ', '-')


# @register.simple_tag(takes_context=True)
# def pcoi_group(context, category_url):
#     """
#     Groups PlanCategoryOnlineIdea instances by category.
#     Args:
#         category: category for which the user has selected at least one idea.
#     Returns:
#         Queryset
#     """
#     pcoi = context['pcoi']
#     group_by_category =pcoi.filter(category__category_url=category_url)
#     category_name = group_by_category[0].category
#     #return group_by_category,category_name
#     return {'group_by_category':group_by_category, 'category_name':category_name }

@register.simple_tag(takes_context=True)
def remaining_categories(context, all_categories):
    """
    Computes the (set) difference between all categories/building blocks and the categories for which user has chosen at least one idea.
    """
    #Set that contains the names of the categories for which user has chosen at least one idea
    c_done = context['category_done_summary']
    remaining_c = set([c_name for c_name, _ in all_categories]) - c_done
    return remaining_c
