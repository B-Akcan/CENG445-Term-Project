from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Map(models.Model):
    class BackgroundColor(models.TextChoices):
        BLUE = "BLUE", _("BLUE")
        RED = "RED", _("RED")
        GREEN = "GREEN", _("GREEN")
        WHITE = "WHITE", _("WHITE")
        BLACK = "BLACK", _("BLACK")
        ORANGE = "ORANGE", _("ORANGE")
        PINK = "PINK", _("PINK")
        GRAY = "GRAY", _("GRAY")
        YELLOW = "YELLOW", _("YELLOW")
        PURPLE = "PURPLE", _("PURPLE")

    id = models.IntegerField(primary_key=True)
    num_cols = models.IntegerField()
    num_rows = models.IntegerField()
    cellsize = models.IntegerField()
    bg_color = models.CharField(max_length=10, choices=BackgroundColor.choices, default=BackgroundColor.WHITE)
    users = models.ManyToManyField(User, related_name="maps")

    def __str__(self):
        return " ".join([str(self.id), str(self.num_cols), str(self.num_rows), str(self.cellsize), str(self.bg_color)])

class ComponentRegistry(models.Model):
    type = models.CharField(primary_key=True, max_length=20)
    is_registered = models.BooleanField()

class Component(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    type = models.ForeignKey(ComponentRegistry, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    rotation = models.IntegerField(default=0)

    def __str__(self):
        return " ".join([str(self.map.id), str(self.type.type), str(self.x), str(self.y), str(self.rotation)])
    
class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    model = models.CharField(max_length=20)
    driver = models.CharField(max_length=20)
    topspeed = models.FloatField()
    topfuel = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['map', 'model'], name="map_model"
            )
        ]

    def __str__(self):
        return " ".join([str(self.id), str(self.map.id), str(self.model), str(self.driver), str(self.topspeed), str(self.topfuel)])
