import datetime

from django.db.models import Avg, Count
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from recom.models import Movie


class IndexView(generic.TemplateView):
    template_name = 'recom/index.html'


class MovieBestListView(generic.ListView):
    model = Movie
    template_name = 'recom/movie_list.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Best Movies"
        return data


class MovieTrendListView(generic.ListView):
    model = Movie
    template_name = 'recom/movie_list.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.filter(points__date__gte=datetime.date.today() - datetime.timedelta(days=7)).annotate(
            counts=Count('points'), avg_point=(Avg('points__point'))).order_by('-counts')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Trend Movies"
        return data


class MovieIndex(generic.ListView):
    model = Movie
    template_name = 'recom/movie_index.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["trends"] = self.model.objects.filter(
            points__date__gte=datetime.date.today() - datetime.timedelta(days=7)).annotate(counts=Count('points'),
                                                                                           avg_point=(Avg(
                                                                                               'points__point'))).order_by(
            '-counts')[:11]  ## Son 7 güne ait puan ortalamasını getiriyor
        return data


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'recom/movie_detail.html'