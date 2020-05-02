from django import template
from django.urls import reverse

from recom.models import Movie, Book, Music, PieceBaseModel

register = template.Library()

@register.simple_tag
def get_url(pk):
    for model in [Movie, Book, Music]:
        if model.objects.filter(pk=pk).exists():
            return reverse("recom:{}_detail".format(model.__name__.lower()), args=(pk,))


@register.filter
def is_wished(pk, user):
    return user.wishes.objects.filter(pk=pk).exists()


@register.filter
def is_followed(pk, user):
    return user.follows.objects.filter(pk=pk).exists()
