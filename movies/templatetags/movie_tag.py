from django import template

from movies.models import Category, Movie


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('movies/tags/recent_movies.html')
def get_recent_movies(count=3):
    movies = Movie.objects.filter(draft=False).order_by('-id')[:count]
    return {'recent_movies': movies}
