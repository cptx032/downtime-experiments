from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=512)


class Person(models.Model):
    name = models.CharField(max_length=512)
    tag = models.ForeignKey(
        Tag, null=True, blank=True, on_delete=models.CASCADE
    )
