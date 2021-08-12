from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=512)


class Person(models.Model):
    name = models.CharField(max_length=512)
    age = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("name", "age")
