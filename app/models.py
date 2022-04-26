from django.db import models


class Station(models.Model):
    call_sign = models.CharField(max_length=4)
    url = models.URLField()

    def __str__(self):
        return self.call_sign
