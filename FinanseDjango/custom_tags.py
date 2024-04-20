# custom_tags.py

from django import template

register = template.Library()


@register.simple_tag
def vue_component(component_name, props):
    # Przygotuj atrybuty HTML na podstawie props
    html_attributes = ' '.join(f'data-{key}="{value}"' for key, value in props.items())
    return f'<div {html_attributes}></div>'
