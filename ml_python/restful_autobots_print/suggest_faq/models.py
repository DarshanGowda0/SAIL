from __future__ import unicode_literals

from django.db import models

#this model contains the details about each user


class SuperUsers(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, blank=True, default='')
    password = models.CharField(max_length=100, blank=True, default='')
    api_key = models.CharField(max_length=20, blank=True, default='')


class Users(models.Model):
    owner = models.ForeignKey('SuperUsers', related_name='suggest_faq')
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, blank=True, default='')
    password = models.CharField(max_length=100, blank=True, default='')
    api_key = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        ordering = ('created',)

class Tables(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(Users,on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

class messages(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=True, default = '')
    message = models.TextField()
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ('created',)

class tags(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=True, default = '')
    reply = models.TextField()
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ('created',)


class RightPredictions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=False, default='no tag')
    message = models.TextField()
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, default=1)
    class Meta:
        ordering = ('created',)

class WrongPredictions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=100, blank=False, default='no tag')
    message = models.TextField()
    retag = models.CharField(max_length=100, blank=True, default='')
    table = models.ForeignKey(Tables, on_delete=models.CASCADE, default=1)
    class Meta:
        ordering = ('created',)
