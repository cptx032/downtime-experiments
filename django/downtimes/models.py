from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=512)


class Person(models.Model):
    last_name = models.CharField(max_length=512)
