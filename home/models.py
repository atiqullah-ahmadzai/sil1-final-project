from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FlowData(models.Model):
    
    name = models.CharField(max_length=100)
    data = models.JSONField()
    prediction = models.CharField(max_length=100,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class FirewallStatus(models.Model):
    
    ip     = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Settings(models.Model):
    
    config_key     = models.CharField(max_length=100)
    config_value   = models.CharField(max_length=100,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allowed_ip   = models.JSONField(blank=True)
    allowed_port = models.JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Settings"