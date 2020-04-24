from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from recom.models import Movie


class IndexView(generic.TemplateView):
    template_name = 'recom/index.html'


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'recom/movie_list.html'
    context_object_name = "movies"


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'recom/movie_detail.html'