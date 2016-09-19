from rest_framework import generics
from rest_framework import serializers
from .models import DataModel
from .filters import DataModelFilter


class DataModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DataModel


class ListView(generics.ListAPIView):
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()
    filter_class = DataModelFilter
