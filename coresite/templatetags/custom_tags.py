from django import template

register = template.Library()


@register.filter
def review_in_category(review, anime):
    return review.filter(anime=anime)
