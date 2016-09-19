from .models import DataModel
import django_filters


class DataModelFilter(django_filters.FilterSet):
    class Meta:
        model = DataModel
        fields = {
            'id': ['exact'],
            'value': ['exact', 'gt', 'gte', 'lt', 'lte']
        }
