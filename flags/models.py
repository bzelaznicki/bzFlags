from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

def generate_api_key():
    return str(uuid4())

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=32, unique=True)
    api_key = models.CharField(max_length=36, unique=True, default=generate_api_key)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Flag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key = models.CharField(max_length=32)
    enabled = models.BooleanField(default=True)
    rollout_percentage = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)], default= 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [["project", "key"]]


class FlagOverride(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE)
    user_identifier = models.CharField(max_length=32)
    enabled = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["flag", "user_identifier"]]
