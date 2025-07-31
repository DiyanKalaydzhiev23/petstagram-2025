from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_query_append(context, field, value):
    query_params = context['request'].GET.copy()  # request.GET is read-only
    query_params[field] = value
    # {'text': 'sasho', 'page': 1} -> text=sasho&page=1
    return query_params.urlencode()