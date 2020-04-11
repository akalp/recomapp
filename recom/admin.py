from django.contrib import admin
from recom.models import User, PieceBaseModel, Music, MusicGenre, Movie, MovieGenre, Book, BookGenre, Point, Comment, Author, Director, Performer, Singer, Album
# Register your models here.

admin.site.register(User)
admin.site.register(PieceBaseModel)
admin.site.register(Music)
admin.site.register(MusicGenre)
admin.site.register(Movie)
admin.site.register(MovieGenre)
admin.site.register(Book)
admin.site.register(BookGenre)
admin.site.register(Point)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Director)
admin.site.register(Performer)
admin.site.register(Singer)
admin.site.register(Album)