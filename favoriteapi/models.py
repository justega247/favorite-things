from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from simple_history.models import HistoricalRecords

User = get_user_model()


class Category(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category


class Favorite(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    ranking = models.PositiveIntegerField()
    metadata = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="favorite", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="favorite",  on_delete=models.DO_NOTHING)
    history = HistoricalRecords(
        table_name='favorite_things_history',
        cascade_delete_history=True,
        excluded_fields=['modified_at', 'metadata']
    )

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    class Meta:
        ordering = ['ranking']
