from django.db import models
from library.models import Library


class Pool(models.Model):
    name = models.CharField('Name', max_length=100)
    libraries = models.ManyToManyField(Library, blank=True)

    def __str__(self):
        return self.name