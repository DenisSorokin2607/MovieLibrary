from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from . import models


class MovieAdminForm(forms.ModelForm):
	description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

	class Meta:
		model = models.Movie
		fields = '__all__'


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'url')
	list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
	"""Отзывы на странице фильма"""
	model = models.Reviews
	extra = 1
	readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
	"""Кадры из фильма на странице фильма"""
	model = models.MovieShots
	extra = 1
	readonly_fields = ('get_image', )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

	get_image.short_description = 'Изображение'


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url', 'draft')
	list_filter = ('category', 'year')
	search_fields = ('title', 'category__name')
	inlines = [MovieShotsInline, ReviewInline]
	save_on_top = True
	save_as = True
	list_editable = ('draft',)
	readonly_fields = ('get_image', )
	form = MovieAdminForm
	actions = ['publish', 'unpublish']
	fieldsets = (
		(None, {
			'fields': (('title', 'tagline'), )
		}),
		(None, {
			'fields': ('description', ('poster', 'get_image'), )
		}),
		(None, {
			'fields': (('year', 'world_premier', 'country'), )
		}),
		('Actors', {
			'classes': ('collapse',),
			'fields': (('directors', 'actors', 'genres', 'category'), )
		}),
		(None, {
			'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
		}),
		('Options', {
			'fields': (('url', 'draft'), )
		}),
	)

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.poster.url} width="100" height="100">')

	def unpublish(self, request, queryset):
		"""Снять с публикации"""
		row_update = queryset.update(draft=True)
		if row_update == 1:
			message_bit = '1 запись обновлена'
		else:
			message_bit = f'{row_update} записи обновлены'
		self.message_user(request, f'{message_bit}')

	def publish(self, request, queryset):
		"""Опубликовать"""
		row_update = queryset.update(draft=False)
		if row_update == 1:
			message_bit = '1 запись обновлена'
		else:
			message_bit = f'{row_update} записи обновлены'
		self.message_user(request, f'{message_bit}')

	get_image.short_description = 'Постер'

	unpublish.short_description = 'Снять с публикации'
	unpublish.allowed_permissions = ('change', )

	publish.short_description = 'Опубликовать'
	publish.allowed_permissions = ('change',)


@admin.register(models.Reviews)
class ReviewsAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'parent', 'movie', 'id')
	readonly_fields = ('name', 'email')


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
	list_display = ('name', 'age', 'get_image')
	readonly_fields = ('get_image', )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="50" height="45">')

	get_image.short_description = 'Изображение'


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name', 'url')


@admin.register(models.MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
	list_display = ('title', 'movie', 'get_image')
	readonly_fields = ('get_image', )

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="50" height="45">')

	get_image.short_description = 'Изображение'


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ('movie', 'ip')


admin.site.register(models.RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
