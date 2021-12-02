# from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filter
import django_filters
from .models import Item


class ItemFilter(filter.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Item
        fields = ["author", "created_at", "type"]
