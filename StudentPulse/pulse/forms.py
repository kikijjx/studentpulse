from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import *

from mat_test import get_mat
from pulse.models import *
from ratings_test import get_ratings
from spam_test import get_spam


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']
        spam_score = get_spam(content)
        mat_score = get_mat(content)

        if round(spam_score) == 1:
            raise forms.ValidationError("Отзыв содержит спам")

        if round(mat_score) == 1:
            raise forms.ValidationError("Отзыв содержит нецензурную лексику")

        return content

    def save(self, commit=True):
        review = super().save(commit=False)
        ratings = get_ratings(self.cleaned_data['content'])

        review.rating_criterion1 = round(round(ratings[0], 3))
        review.rating_criterion2 = round(round(ratings[1], 3))
        review.rating_criterion3 = round(round(ratings[2], 3))
        review.rating_criterion4 = round(round(ratings[3], 3))





        if commit:
            review.save()

        return review
