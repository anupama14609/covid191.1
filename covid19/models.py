from django.db import models


# Create your models here.
class CovidUpdate(models.Model):
    search = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.search)