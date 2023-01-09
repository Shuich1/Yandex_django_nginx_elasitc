from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('name', 'description')


class RatingListFilter(admin.SimpleListFilter):
    title = _('Rating')

    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('1-2', _('1-2')),
            ('3-4', _('3-4')),
            ('5-6', _('5-6')),
            ('7-8', _('7-8')),
            ('9-10', _('9-10')),
        )

    def queryset(self, request, queryset):
        return queryset.filter(
            rating__range=self.value().split('-') if self.value() else (1, 10)
        )


class GenreListFilter(admin.SimpleListFilter):
    title = _('Genre')

    parameter_name = 'genre'

    def lookups(self, request, model_admin):
        return (
            ('Action', _('Action')),
            ('Adventure', _('Adventure')),
            ('Fantasy', _('Fantasy')),
            ('Sci-Fi', _('Sci-Fi')),
            ('Drama', _('Drama')),
            ('Music', _('Music')),
            ('Romance', _('Romance')),
            ('Thriller', _('Thriller')),
            ('Mystery', _('Mystery')),
            ('Comedy', _('Comedy')),
            ('Animation', _('Animation')),
            ('Family', _('Family')),
            ('Biography', _('Biography')),
            ('Musical', _('Musical')),
            ('Crime', _('Crime')),
            ('Short', _('Short')),
            ('Western', _('Western')),
            ('Documentary', _('Documentary')),
            ('History', _('History')),
            ('War', _('War')),
            ('Game-Show', _('Game-Show')),
            ('Reality-TV', _('Reality-TV')),
            ('Horror', _('Horror')),
            ('Sport', _('Sport')),
            ('Talk-Show', _('Talk-Show')),
            ('News', _('News')),
        )

    def queryset(self, request, queryset):
        return queryset.filter(
            genres__name__contains=self.value()
        ) if self.value() else queryset


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'creation_date', 'rating',)
    list_filter = ('type', 'creation_date', RatingListFilter, GenreListFilter,)
    search_fields = ('title', 'description', 'id')
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('full_name',)
