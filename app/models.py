from django.db import models


class Station(models.Model):
    call_sign = models.CharField(max_length=4)
    url = models.URLField()

    def __str__(self):
        return self.call_sign


class ScheduledItemManager(models.Manager):
    def create_request(self, url, output_name, start_time, end_time):
        request = self.create(url=url, output_name=output_name, start_time=start_time, end_time=end_time)
        return request


class ScheduledItem(models.Model):
    url = models.URLField()
    output_name = models.CharField(max_length=255)
    start_time = models.CharField(max_length=8)
    end_time = models.CharField(max_length=8)

    objects = ScheduledItemManager()
