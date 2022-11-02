from django import template
from tbcore.models import Category
import markdown

register = template.Library()


@register.filter(name='add_hyphen')
def add_hyphen(value):
    """
    Replaces blank spaces with a hyphen
    """
    return value.replace(' ', '-')


@register.simple_tag()
def get_name_next_category(value):
    """
    Retrieves the name of the next category
    """
    c = Category.objects.get(category_url=value)
    c_name = c.category_name
    c_next = c.next_page
    return {'c_name': c_name, 'c_next': c_next}


@register.simple_tag(takes_context=True)
def remaining_categories(context, all_categories):
    """
    Computes the (set) difference between all categories/building blocks and the categories for which user has chosen
    at least one idea.
    Args:
        context: current template context
        all_categories: List of tuples, where each element (tuple) contains (category_name, category_url)
    """
    # Set that contains the names of the categories for which user has chosen at least one idea
    c_done = context['category_done_summary']
    remaining_c = set([c_name for c_name, _, _ in all_categories]) - c_done
    return remaining_c


@register.simple_tag()
def md_to_html(value):
    return markdown.markdown(value)


@register.simple_tag()
def task_complexity_to_int(value):
    """
    Converts task complexity to int or returns 'no-data'
    """

    try:
        num_stars= int(value)
        list_starts = ['star' for i in range(num_stars)]
        return list_starts
    except ValueError:
        print('Task complexity must be of type int')
        return 'no-data'
