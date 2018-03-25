from django.db import models
from django.db.models.signals import post_save # we will now define signals so our Profile model will be
from django.dispatch import receiver           #automatically created/updated when we create/update User instances.
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=500)
    gender = models.CharField(max_length=10)
    job_position = models.CharField(max_length=20)
    salary = models.IntegerField()

    def __str__(self):
        return self.emp_name

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    employees = models.ManyToManyField(Profile)

    def __str__(self):
        return self.project_name

class TimeSheet(models.Model):
    profile = models.ManyToManyField(Profile)
    emp_name = models.CharField(max_length=100, default='emp_name')
    date  = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #project_name = models.CharField(max_length=100, default='project_name')
    def __str__(self):
        return self.emp_name + ' ' + self.project.project_name +' '+ str(self.date)
