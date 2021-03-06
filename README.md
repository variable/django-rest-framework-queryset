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
    girls = qs.filter(gender='girl')
    
    # get by id
    boy = qs.get(101)
    
    # filter enforce 1 result
    boy = qs.get(name='james', gender='boy')

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
The queryset is dependent on the API that uses [LimitOffsetPagination](http://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination)

In this project, it provides a HybridPagination class, which will swap to `LimitOffsetPagination` when it sees `limit` or `offset` query params,
so that if you are currently using `PageNumberPagination` then you can swap it 
with `rest_framework_queryset.pagination.HybridPagination` to achieve both purposes. This feature is experimental, so please report any problems.

## Compatibility 
- Python 2
- Python 3
