from django.db import models
from accounts.models import Profile, Project
# Create your models here.
class Supervisor(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    sup_name = models.CharField(max_length=200, default='sup_name')
    projects = models.ManyToManyField(Project)
    def __str__(self):
        return self.sup_name
