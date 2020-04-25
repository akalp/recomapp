import datetime

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Case, When, IntegerField, Q
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
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Trend Movies"
        return data


class MovieIndex(generic.ListView):
    model = Movie
    template_name = 'recom/movie_index.html'
    context_object_name = "movies"

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)

        data["bests"] = self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_{} m, recom_piecebasemodel b, recom_point p, recom_user u where m.piecebasemodel_ptr_id = b.id and p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc".format("movie")
        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'recom/movie_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print(kwargs)
        data["full_pointers"] = get_user_model().objects.filter(Q(points__point=5) & Q(points__piece_id=kwargs['object']))
        return data
