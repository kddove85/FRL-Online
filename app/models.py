from django.db import models


class Station(models.Model):
    call_sign = models.CharField(max_length=4)
    url = models.URLField()

    def __str__(self):
        return self.call_sign


class Weekday(models.Model):
    day = models.CharField(max_length=10)
    value = models.IntegerField()

    def __str__(self):
        return self.day


class ScheduledItemManager(models.Manager):
    def create_request(self, url, output_name, day_of_the_week, start_time, end_time):
        request = self.create(url=url, output_name=output_name, day_of_the_week=day_of_the_week, start_time=start_time,
                              end_time=end_time)
        return request


class ScheduledItem(models.Model):
    url = models.URLField()
    output_name = models.CharField(max_length=255)
    day_of_the_week = models.IntegerField()
    start_time = models.CharField(max_length=8)
    end_time = models.CharField(max_length=8)

    objects = ScheduledItemManager()

    def day_of_the_week_to_string(self):
        switcher = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        return switcher.get(self.day_of_the_week, "None Selected")

