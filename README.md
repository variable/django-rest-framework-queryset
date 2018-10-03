[![Build Status](https://travis-ci.org/variable/django-rest-framework-queryset.svg?branch=master)](https://travis-ci.org/variable/django-rest-framework-queryset)
# Django Rest Framework QuerySet
Mimicking the Django ORM queryset over rest framework api, which does lazy loading.

## Usage:

### normal operation
```python
    from rest_framework_queryset import RestFrameworkQuerySet
    from django.core.paginator import Paginator

    qs = RestFrameworkQuerySet('http://localhost:8082/api/')

    # filter
    boys = qs.filter(gender='boy')
    girls = qs.filter(gender='girls')

    # slicing
    first_100_boys = boys[:100]
    
    # iterate all records
    for i in qs:
        print(i)

    # pagination
    p = Paginator(qs, 10)
    print p.count
    print p.num_pages
    page1 = p.page(1)
```

### class based view
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
