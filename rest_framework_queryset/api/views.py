from rest_framework import generics
from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    value = serializers.IntegerField()


class ListView(generics.ListAPIView):
    serializer_class = DataSerializer
    queryset = [{'value': i} for i in range(100)]
