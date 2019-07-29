from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator
from simple_history.models import HistoricalRecords

User = get_user_model()


class Category(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['category']


class Favorite(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(
        validators=[MinLengthValidator(10, message='Please provide a description with more than ten characters')],
        max_length=300, blank=True)
    ranking = models.PositiveIntegerField()
    metadata = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name="favorite",  on_delete=models.DO_NOTHING)
    history = HistoricalRecords(
        table_name='favorite_things_history',
        cascade_delete_history=True,
        excluded_fields=['modified_at', 'metadata']
    )

    def __str__(self):
        return self.title

    @property
    def category_name(self):
        return self.category.category

    class Meta:
        ordering = ['ranking']
