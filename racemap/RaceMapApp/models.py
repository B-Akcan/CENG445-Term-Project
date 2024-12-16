from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Map(models.Model):
    id = models.IntegerField(primary_key=True)
    num_cols = models.IntegerField()
    num_rows = models.IntegerField()
    cellsize = models.IntegerField()
    bg_color = models.CharField(max_length=20)
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
    

