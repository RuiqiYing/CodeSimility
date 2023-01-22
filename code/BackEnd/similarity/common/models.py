from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.IntegerField()
    ctime = models.DateTimeField(blank=True, null=True)
    information = models.CharField(max_length=200)
    userid=models.CharField(max_length=200,primary_key=True)
    class Meta:
        managed = True
        db_table = 'user'