import datetime

from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Avg, Count, When, Case, IntegerField, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import generic

from recom.models import PieceBaseModel, Movie, Book, Music
from recom.forms import UserForm, UserEditForm
from recom.templatetags.extras import get_url


class IndexView(generic.TemplateView):
    template_name = 'recom/index.html'
    model = PieceBaseModel

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_piecebasemodel b, recom_point p, recom_user u where p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc"
        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


## MOVIE
class MovieIndex(generic.ListView):
    model = Movie
    template_name = 'recom/movie_index.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:11]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)

        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_{} m, recom_piecebasemodel b, recom_point p, recom_user u where m.piecebasemodel_ptr_id = b.id and p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc".format(
            "movie")
        data["active_users"] = get_user_model().objects.raw(act_user_query)[:11]
        return data


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'recom/movie_list.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Movies"
        return data


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


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'recom/movie_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["full_pointers"] = get_user_model().objects.filter(
            Q(points__point=5) & Q(points__piece_id=kwargs['object']))
        return data


## MUSIC
class MusicIndex(generic.ListView):
    model = Music
    template_name = 'recom/music_index.html'
    context_object_name = "music"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:11]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),

                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by('-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_{} m, recom_piecebasemodel b, recom_point p, recom_user u where m.piecebasemodel_ptr_id = b.id and p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc".format(
            "music")

        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


class MusicListView(generic.ListView):
    model = Music
    template_name = 'recom/music_list.html'
    context_object_name = "musics"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Musics"
        return data


class MusicBestListView(generic.ListView):
    model = Music
    template_name = 'recom/music_list.html'
    context_object_name = "music"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Best Music"
        return data


class MusicTrendListView(generic.ListView):
    model = Music
    template_name = 'recom/music_list.html'
    context_object_name = "music"

    def get_queryset(self):
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by('-counts')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Trend Music"
        return data


class MusicDetailView(generic.DetailView):
    model = Music
    template_name = 'recom/music_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["full_pointers"] = get_user_model().objects.filter(
            Q(points__point=5) & Q(points__piece_id=kwargs['object']))
        return data


## BOOK
class BookIndex(generic.ListView):
    model = Book
    template_name = 'recom/book_index.html'
    context_object_name = "books"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:11]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:11]
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:11]

        act_user_query = "select u.*, count(p.id) as count from recom_{} m, recom_piecebasemodel b, recom_point p, recom_user u where m.piecebasemodel_ptr_id = b.id and p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc".format(
            "book")
        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


class BookListView(generic.ListView):
    model = Book
    template_name = 'recom/book_list.html'
    context_object_name = "books"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Books"
        return data


class BookBestListView(generic.ListView):
    model = Book
    template_name = 'recom/book_list.html'
    context_object_name = "books"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point'))).order_by('-avg_point')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Best Books"
        return data


class BookTrendListView(generic.ListView):
    model = Book
    template_name = 'recom/book_list.html'
    context_object_name = "books"

    def get_queryset(self):
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by('-counts')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["page_title"] = "Trend Books"
        return data


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'recom/book_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["full_pointers"] = get_user_model().objects.filter(
            Q(points__point=5) & Q(points__piece_id=kwargs['object']))
        return data


## USER
class UserDetailView(generic.DetailView):
    model = get_user_model()
    context_object_name = 'user_profile'
    template_name = 'recom/profile.html'


class UserEditView(generic.UpdateView):
    model = get_user_model()
    template_name = 'recom/user_edit.html'
    form_class = UserEditForm


def login_register(request):
    registered = False

    if request.method == 'GET':
        user_form = UserForm()
        return render(request=request, template_name='login_register.html',
                      context={'user_form': user_form, 'registered': registered, 'from_log': True})
    else:
        where = request.GET["from"]
        if where == "login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username)
            print(password)

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                return HttpResponseRedirect(next if next else reverse('recom:user_detail', kwargs={'pk': user.pk}))
            else:
                user_form = UserForm()
                return render(request=request, template_name='login_register.html',
                              context={'error': True, 'user_form': user_form, 'from_log': True})
        elif where == "register":
            user_form = UserForm(data=request.POST)
            print(request.FILES)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)

                if 'profile_photo' in request.FILES:
                    print("test")
                    new_user.profile_photo = request.FILES['profile_photo']
                new_user.save()
                registered = True
                next = request.GET.get('next')
                return HttpResponseRedirect(next if next else reverse('recom:login_register'))
            return render(request=request, template_name='login_register.html',
                          context={'user_form': user_form, 'registered': registered, 'from_reg': True})
        else:
            HttpResponse("Impossible!")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('recom:index'))


## Operations
@login_required
def wish(request, pk):
    piece = PieceBaseModel.objects.get(pk=pk)
    request.user.wishes.add(piece)
    request.user.save()
    return HttpResponseRedirect(get_url(pk))


@login_required
def del_wish(request, pk):
    piece = PieceBaseModel.objects.get(pk=pk)
    request.user.wishes.remove(piece)
    request.user.save()
    return HttpResponseRedirect(get_url(pk))


@login_required
def follow_user(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.followed_by.add(request.user)
    user.save()
    return redirect('recom:user_detail', pk=user.pk)


@login_required
def unfollow_user(request, pk):
    user = get_user_model().objects.get(pk=pk)
    user.followed_by.remove(request.user)
    user.save()
    return redirect('recom:user_detail', pk=user.pk)
