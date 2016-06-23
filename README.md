# Django Rest Framework QuerySet
Mimicking the Django ORM queryset over rest framework api

## Usage:
```python
from django.views.generic import ListView
from rest_framework_queryset import RestFrameworkQuerySet

class ListDataView(ListView):
    paginate_by = 10
    template_name = 'list.html'

    def get_queryset(self, *args, **kwargs):
        return RestFrameworkQuerySet('http://localhost:8082/api/').filter(**self.request.GET.dict())
```

## Dependencies
The queryset is dependent on the API that uses [LimiteOffsetPagination](http://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination)
If you are using [PageNumberPagination](http://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination) then you can use the included `rest_framework_queryset.pagination.HybridPagination` which will switch pagination class depends on the query param is passed.
