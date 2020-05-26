from django import template
from django.urls import reverse

from recom.models import Movie, Book, Music, PieceBaseModel

register = template.Library()

@register.simple_tag
def get_url(pk):
    for model in [Movie, Book, Music]:
        if model.objects.filter(pk=pk).exists():
            return reverse("recom:{}_detail".format(model.__name__.lower()), args=(pk,))


@register.simple_tag
def get_type(pk):
    for model in [Movie, Book, Music]:
        if model.objects.filter(pk=pk).exists():
            return model.__name__


@register.simple_tag
def get_genre(pk):
    for model in [Movie, Book, Music]:
        piece = model.objects.filter(pk=pk)
        if piece.exists():
            return piece.first().genre.name


@register.simple_tag
def get_point(object, user):
    query = object.points.filter(user=user)
    if query.exists():
        return query.first().point
    else:
        return 0


@register.filter
def is_wished(pk, user):
    return user.wishes.filter(pk=pk).exists()


@register.filter
def is_followed(pk, user):
    return user.follows.filter(pk=pk).exists()


@register.filter
def is_liked_comment(pk, user):
    return user.liked_comments.filter(pk=pk).exists()
