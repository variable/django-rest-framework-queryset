from rest_framework import generics
from rest_framework import serializers
from rest_framework import viewsets
from .models import DataModel
from .filters import DataModelFilter


class DataModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DataModel
        fields = '__all__'


class ListView(viewsets.ModelViewSet):
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()
    filter_class = DataModelFilter
