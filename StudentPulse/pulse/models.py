from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    rating_criterion1 = models.FloatField()
    rating_criterion2 = models.FloatField()
    rating_criterion3 = models.FloatField()
    rating_criterion4 = models.FloatField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.lesson.title}"