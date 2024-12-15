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

class ComponentRegistry(models.Model):
    type = models.CharField(primary_key=True, max_length=20)
    is_registered = models.BooleanField()

class Component(models.Model):
    class RotationChoices(models.IntegerChoices):
        ZERO = 0, _("ZERO")
        ONE = 1, _("ONE")
        TWO = 2, _("TWO")
        THREE = 3, _("THREE")

    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    type = models.ForeignKey(ComponentRegistry, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    rotation = models.IntegerField(choices=RotationChoices.choices, default=RotationChoices.ZERO)

