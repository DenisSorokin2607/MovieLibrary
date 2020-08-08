from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):
	"""Форма отзывов"""
	class Meta:
		model = Reviews
		fields = ('email', 'name', 'text')
