from django import template
from django.urls import reverse

from recom.models import Movie, Book, Music

register = template.Library()

@register.simple_tag
def get_url(pk):
    for model in [Movie, Book, Music]:
        if model.objects.filter(pk=pk).exists():
            return reverse("recom:{}_detail".format(model.__name__.lower()), args=(pk,))