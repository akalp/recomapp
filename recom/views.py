import datetime

from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.db.models import Avg, Count, When, Case, IntegerField, Q, F
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from recom.models import PieceBaseModel, Movie, Book, Music, Point, Comment
from recom.forms import UserForm, UserEditForm
from recom.templatetags.extras import get_url


class IndexView(generic.TemplateView):
    template_name = 'recom/index.html'
    model = PieceBaseModel

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:10]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:10]

        act_user_query = "select u.*, count(p.id) as count from recom_piecebasemodel b, recom_point p, recom_user u where p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc"
        data["active_users"] = get_user_model().objects.raw(act_user_query)
        return data


## MOVIE
class MovieIndex(generic.ListView):
    model = Movie
    template_name = 'recom/movie_index.html'
    context_object_name = "movies"

    def get_queryset(self):
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:10]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)

        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:10]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:10]

        act_user_query = "select u.*, count(p.id) as count from recom_{} m, recom_piecebasemodel b, recom_point p, recom_user u where m.piecebasemodel_ptr_id = b.id and p.piece_id=b.id and p.user_id=u.id group by u.id order by count desc".format(
            "movie")
        data["active_users"] = get_user_model().objects.raw(act_user_query)[:10]
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

    def get_queryset(self):
        return self.model.objects.annotate(
            avg_point=(Avg('points__point')))

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
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:10]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:10]
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),

                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by('-counts')[:10]

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

    def get_queryset(self):
        return self.model.objects.annotate(
            avg_point=(Avg('points__point')))

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
        return self.model.objects.all().annotate(avg_point=(Avg('points__point')))[:10]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["bests"] = self.model.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:10]
        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trends"] = self.model.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:10]

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

    def get_queryset(self):
        return self.model.objects.annotate(
            avg_point=(Avg('points__point')))

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


## COMMENT
def make_comment(request):
    if request.is_ajax():
        if request.method == "POST":
            user = get_user_model().objects.get(pk=request.POST.get('user'))
            piece = PieceBaseModel.objects.get(pk=request.POST.get('piece'))
            comment = request.POST.get('comment')
            point = request.POST.get('point')

            obj = Comment()
            obj.user = user
            obj.piece = piece
            obj.text = comment
            obj.point = point
            obj.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'msg': 'GET method is not allowed!'})

    return HttpResponse("This process is not valid.")


## Operations
@login_required
def like_comment(request, pk):
    obj = Comment.objects.get(pk=pk)
    piece_pk = obj.piece.pk
    request.user.liked_comments.add(obj)
    request.user.save()
    where = request.GET.get('from')
    if where == "profile":
        return HttpResponseRedirect(reverse('recom:user_detail', kwargs={"pk": request.user.pk}))
    elif where == "dashboard":
        return HttpResponseRedirect(reverse('recom:dashboard'))
    else:
        return HttpResponseRedirect(get_url(piece_pk))


@login_required
def unlike_comment(request, pk):
    obj = Comment.objects.get(pk=pk)
    piece_pk = obj.piece.pk
    request.user.liked_comments.remove(obj)
    request.user.save()
    where = request.GET.get('from')
    if where == "profile":
        return HttpResponseRedirect(reverse('recom:user_detail', kwargs={"pk": request.user.pk}))
    elif where == "dashboard":
        return HttpResponseRedirect(reverse('recom:dashboard'))
    else:
        return HttpResponseRedirect(get_url(piece_pk))


@login_required
def del_comment(request, pk):
    obj = Comment.objects.get(pk=pk)
    piece_pk = obj.piece.pk
    obj.delete()
    where = request.GET.get('from')
    if where == "profile":
        return HttpResponseRedirect(reverse('recom:user_detail', kwargs={"pk": request.user.pk}))
    else:
        return HttpResponseRedirect(get_url(piece_pk))


## POINT
def give_point(request):
    if request.is_ajax():
        if request.method == "POST":
            user = get_user_model().objects.get(pk=request.POST.get('user'))
            piece = PieceBaseModel.objects.get(pk=request.POST.get('piece'))
            point = request.POST.get('point')

            query = Point.objects.filter(user=user, piece=piece)
            if query.exists():
                obj = query.first()
                obj.point = point
                obj.save()
            else:
                obj = Point()
                obj.user = user
                obj.point = point
                obj.piece = piece
                obj.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'msg': 'GET method is not allowed!'})
    else:
        return HttpResponse("This process is not valid.")


def get_avg_point(request, pk):
    if request.is_ajax():
        if request.method == "GET":
            piece = PieceBaseModel.objects.filter(pk=pk).annotate(avg_point=(Avg('points__point'))).first()
            return JsonResponse({"success": True, "avg_point": piece.avg_point})
        else:
            return JsonResponse({"success": False})
    else:
        return HttpResponse("This process is not valid.")


class Dashboard(generic.ListView):
    model = Comment
    context_object_name = "comments"
    template_name = 'recom/dashboard.html'

    def get_queryset(self):
        return self.model.objects.filter(user__followed_by=self.request.user.pk).order_by('-date')


class WishesListView(generic.ListView):
    model = PieceBaseModel
    context_object_name = "objects"
    template_name = "recom/wishes.html"

    def get_queryset(self):
        return self.model.objects.filter(wished_by=self.kwargs.get('user_pk'))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["title"] = "{} Wishes".format(get_user_model().objects.get(pk=self.kwargs.get('user_pk')).username)
        return data


class WishedByListView(generic.ListView):
    model = get_user_model()
    context_object_name = "objects"
    template_name = "recom/wished.html"

    def get_queryset(self):
        return self.model.objects.filter(wishes=self.kwargs.get('piece_pk'))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["title"] = "{} Wished By".format(PieceBaseModel.objects.get(pk=self.kwargs.get('piece_pk')).name)
        return data


class FollowsListView(generic.ListView):
    model = get_user_model()
    context_object_name = "objects"
    template_name = "recom/wished.html"

    def get_queryset(self):
        return self.model.objects.filter(followed_by=self.kwargs.get('user_pk'))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["title"] = "{} Follows".format(get_user_model().objects.get(pk=self.kwargs.get('user_pk')).username)
        return data


class FollowerListView(generic.ListView):
    model = get_user_model()
    context_object_name = "objects"
    template_name = "recom/wished.html"

    def get_queryset(self):
        return self.model.objects.filter(follows=self.kwargs.get('user_pk'))

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["title"] = "{}'s Followers".format(get_user_model().objects.get(pk=self.kwargs.get('user_pk')).username)
        return data


class SearchListView(generic.ListView):
    template_name = 'recom/search.html'
    context_object_name = 'objects'

    def get_queryset(self):
        search = self.request.GET.get('search')
        return PieceBaseModel.objects.filter(Q(publish_date__lte=timezone.now()),
                                             Q(name__icontains=search) | Q(text__icontains=search)).order_by(
            '-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        context['title'] = "Search: " + search
        context['users'] = get_user_model().objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search))
        return context


class ReportView(generic.TemplateView):
    template_name = "recom/report.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["encoktakipedilenler"] = get_user_model().objects.exclude(pk=1).annotate(follower_count=Count("followed_by")).order_by(
            "-follower_count")[:10]

        data["encokbegenilenyorumlar"] = Comment.objects.annotate(like_count=Count("liked")).order_by("-like_count")[
                                         :10]

        data["encoketkilesimalanparcalar"] = PieceBaseModel.objects.annotate(wish_count=Count("wished_by"),
                                                                             comment_count=Count("comments"),
                                                                             point_count=Count("points")).annotate(
            total=F("wish_count") + F("comment_count") + F("point_count")).order_by("-total")

        data["encoketkilesimverenkullanicilar"] = get_user_model().objects.exclude(pk=1).annotate(
            comment_like_count=Count("liked_comments"), follow_count=Count("follows"), wish_count=Count("wishes"),
            comment_count=Count("comments"),
            point_count=Count("points")).annotate(
            total=F("liked_comments") + F("follows") + F("wish_count") + F("comment_count") + F(
                "point_count")).order_by("-total")

        data["encoketkilesimalankullanicilar"] = get_user_model().objects.exclude(pk=1).annotate(follower_count=Count("followed_by"),
                                                                                   comment_like_count=Count(
                                                                                       "comments__liked")).annotate(
            total=F("follower_count") + F("comment_like_count")).order_by("-total")[:10]
        
        data["bestpieces"] = PieceBaseModel.objects.filter(points__isnull=False).annotate(
            avg_point=(Avg('points__point'))).order_by('-avg_point')[:10]

        trending_time = datetime.date.today() - datetime.timedelta(days=7)
        data["trendpieces"] = PieceBaseModel.objects.all().annotate(avg_point=(Avg('points__point')), counts=Count(
            Case(When(points__date__gte=trending_time, then=1),
                 output_field=IntegerField()))).filter(points__date__gte=trending_time).order_by(
            '-counts')[:10]
        return data
