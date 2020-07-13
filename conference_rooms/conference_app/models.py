from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    has_projector =models.BooleanField(default=False)

class Reservation(models.Model):
    date = models.DateField()
    comment = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['room', 'date']

    def __str__(self):
        return self.date


