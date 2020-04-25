import datetime

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, When, Case, IntegerField
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from recom.models import PieceBaseModel, Movie


class IndexView(generic.TemplateView):
    template_name = 'recom/index.html'
    model = PieceBaseModel

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["bests"] = self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_piecebasemodel b, recom_point p, recom_user u where p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc"
        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'recom/movie_list.html'
    context_object_name = "movies"


class MovieDetailView(generic.DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'recom/movie_detail.html'


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy('recom:movie_list')