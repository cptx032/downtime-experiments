from rest_framework import serializers

from downtimes import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("pk", "name")
