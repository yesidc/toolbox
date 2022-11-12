from django import template
from tbcore.models import Category, OnlineIdea
import markdown
from django.db.models import Count
register = template.Library()




@register.filter(name='add_hyphen')
def add_hyphen(value):
    """
    Replaces blank spaces with a hyphen
    Args:
        value: string
    """

    return value.replace(' ', '-')


@register.simple_tag()
def get_single_category(value):
    """
    Takes as an argument a queryset and returns a single object Category instance
    """
    return  value[0]

@register.simple_tag()
def get_accordion_content(title, content):
    """
    Fetches the content that is eventually displayed using the accordions.
    """

    if len(title) == 0:
        len_content = 0
        return {'len_content': len_content}
    else:

        titles = title.split('[split]')
        c_accordion = content.split('[split]')
        len_content = len(titles)
        content_accordion = tuple([*zip([*range(len_content)], titles, c_accordion)])

    return {'len_content': len_content, 'content_accordion': content_accordion}


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
def remaining_categories(context):
    """
    Computes the (set) difference between all categories/building blocks and the categories for which user has chosen
    at least one idea.
    Args:
        context: current template context
        all_categories: List of tuples, where each element (tuple) contains (category_name, category_url)
    """

    # Some categories do not contain online ideas, hence we must compare user's progress against the CategoryOnlineIdea table.
    idea_grouped_by_c = OnlineIdea.objects.values('category__category_name').annotate(c=Count('category__category_name')).order_by()
    categories_list = [i['category__category_name'] for i in idea_grouped_by_c]

    c_done = context['category_done_summary']

    remaining_c = set(categories_list) - c_done

    return remaining_c


@register.inclusion_tag('plan/show_ideas.html',takes_context=True)
def show_ideas(context,user_authenticated):
    return {
        'ideas': context['ideas'],
        'current_category': context['current_category'],
        'ideas_list':context['ideas_list'],
        'user_authenticated':user_authenticated,
    }


@register.simple_tag()
def md_to_html(value):
    return markdown.markdown(value)


@register.simple_tag()
def task_complexity_to_int(value):
    """
    Converts task complexity to int or returns 'no-data'
    """

    try:
        num_stars = int(value)
        list_starts = ['star' for i in range(num_stars)]
        return list_starts
    except ValueError:
        print('Task complexity must be of type int')
        return 'no-data'
