from django import template

register = template.Library()


@register.filter(name='add_hyphen')
def add_hyphen(value):
    """
    Replaces blank spaces with a hyphen
    """
    return value.replace(' ', '-')




@register.simple_tag(takes_context=True)
def remaining_categories(context, all_categories):
    """
    Computes the (set) difference between all categories/building blocks and the categories for which user has chosen
    at least one idea.
    Args:
        context: current template context
        all_categories: List of tuples, where each element (tuple) contains (category_name, category_url)
    """
    #Set that contains the names of the categories for which user has chosen at least one idea
    c_done = context['category_done_summary']
    remaining_c = set([c_name for c_name, _ in all_categories]) - c_done
    return remaining_c
