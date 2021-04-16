from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [("Completed", "completed"), ("In progress", "in progress"), ("Planned", "Planned")]
    title = models.CharField(max_length=200, name="title")
    description = models.TextField(name="description")
    date_created = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now().strftime("%d.%m.%Y %H:%M"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="In progress")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})