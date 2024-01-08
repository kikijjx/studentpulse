import base64
import io

import qrcode
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate

from mat_test import get_mat
from pulse.forms import *
from pulse.models import *
import os
from django.conf import settings

from ratings_test import get_ratings
from spam_test import get_spam


def base(request):
    if request.user.is_authenticated:
        return redirect('user_profile')

    next_url = request.GET.get('next', None)
    return render(request, 'base.html', {'next_url': next_url})


def user(request):  # httprequest
    return HttpResponse("userz")


def user_profile(request):
    user_lessons = Lesson.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    context = {
        'user_lessons': user_lessons,
        'user_reviews': user_reviews,
    }

    return render(request, 'user_profile.html', context)


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    review_url = request.build_absolute_uri(lesson.get_absolute_url() + 'create_review/')
    qr.add_data(review_url)
    qr.make(fit=True)

    # Создаем папку, если ее нет
    qr_folder = os.path.join(settings.BASE_DIR, 'static', 'qrcodes')
    os.makedirs(qr_folder, exist_ok=True)

    # Генерируем QR-код и сохраняем его
    img = qr.make_image(fill_color="black", back_color="white")

    # Преобразовываем изображение в строку base64
    img_byte_array = io.BytesIO()
    img.save(img_byte_array)
    img_content = ContentFile(img_byte_array.getvalue())
    encoded_img = base64.b64encode(img_content.read()).decode('utf-8')

    return render(request, 'lesson_detail.html', {'lesson': lesson, 'qr_path': encoded_img})




from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем на указанный URL после успешной авторизации
                next_url = request.POST.get('next', None)
                if next_url!='None':
                   return redirect(next_url)
                else:
                   return redirect('user_profile')
    else:
        form = AuthenticationForm()

    return render(request, 'signin.html', {'form': form, 'next_url': request.GET.get('next', None)})


from django.contrib.auth import logout


def custom_logout(request):
    logout(request)
    return redirect('base')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем на указанный URL после успешной авторизации
                next_url = request.POST.get('next', None)
                if next_url != 'None':
                    return redirect(next_url)
                else:
                    return redirect('user_profile')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form, 'next_url': request.GET.get('next', None)})



def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.save()
            return redirect('user_profile')  # Перенаправить обратно на страницу профиля пользователя
    else:
        form = LessonForm()

    return render(request, 'create_lesson.html', {'form': form})

def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user_profile/')  # Перенаправление после редактирования
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'edit_lesson.html', {'form': form, 'lesson': lesson})


def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        lesson.delete()
        return HttpResponseRedirect('/user_profile/')  # Перенаправление после удаления

    return render(request, 'delete_lesson.html', {'lesson': lesson})





@login_required
def create_review(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['content']
            ratings = get_ratings(input_text)

            # Проверка на спам и мат


            # Добавьте оценки в форму
            form.cleaned_data['rating_criterion1'] = ratings[0]
            form.cleaned_data['rating_criterion2'] = ratings[1]
            form.cleaned_data['rating_criterion3'] = ratings[2]
            form.cleaned_data['rating_criterion4'] = ratings[3]

            # Добавьте связь с уроком и пользователем
            review = form.save(commit=False)
            review.lesson = lesson
            review.user = request.user
            review.save()

            return redirect('user_profile')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form, 'lesson': lesson})

def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user_profile/')  # Перенаправление после редактирования
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})


def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review.delete()
        return HttpResponseRedirect('/user_profile/')  # Перенаправление после удаления

    return render(request, 'delete_review.html', {'review': review})