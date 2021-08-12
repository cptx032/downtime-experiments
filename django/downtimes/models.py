from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=512, null=True)


class Person(models.Model):
    name = models.CharField(max_length=512)
