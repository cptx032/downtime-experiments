from rest_framework import generics, status, viewsets

from downtimes import models, serializers


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
