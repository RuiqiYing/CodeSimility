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

class Course(models.Model):
    courseid = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=255)
    classname = models.CharField(max_length=255)
    userid = models.CharField(max_length=200)
    ctime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'course'


class Homework(models.Model):
    homeworkid = models.AutoField(primary_key=True)
    homeworkname = models.CharField(max_length=255)
    courseid = models.CharField(max_length=255)
    questionnum=models.CharField(max_length=255)
    ctime = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'homework'



class QuestionBank(models.Model):
    questionid = models.AutoField(primary_key=True)
    questiontype = models.CharField(max_length=255)
    questionnum = models.CharField(max_length=255)
    # 记录属于哪一套题
    question = models.TextField(max_length=10000)
    optionA = models.TextField(max_length=10000)
    optionB = models.TextField(max_length=10000)
    optionC = models.TextField(max_length=10000)
    optionD = models.TextField(max_length=10000)


    class Meta:
        managed = True
        db_table = 'questionbank'


class Answer (models.Model):
    ansid=models.AutoField(primary_key=True)
    userid=models.CharField(max_length=255)
    questionid = models.CharField(max_length=255)
    question = models.TextField(max_length=10000)
    answer=models.TextField(max_length=10000)
    questiontype = models.CharField(max_length=255)
    highsimilarityA=models.FloatField(default=0.00)
    highsimilarityB = models.FloatField(default=0.00)
    highsimilarityC = models.FloatField(default=0.00)
    questionnum=models.CharField(max_length=255)
    homeworkid=models.CharField(max_length=255)
    selecttype=models.CharField(max_length=255,default="0")
    class Meta:
        managed = True
        db_table = 'answer'


class Joincourse (models.Model):
    jid=models.AutoField(primary_key=True)
    userid=models.CharField(max_length=255)
    courseid=models.CharField(max_length=255)
    classname = models.CharField(max_length=255)
    coursename = models.CharField(max_length=255)
    class Meta:
        managed = True
        db_table = 'joincourse'

