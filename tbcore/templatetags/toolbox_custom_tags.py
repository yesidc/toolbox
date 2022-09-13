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
