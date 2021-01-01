from djongo import models


class App(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)


class Role(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200, null=True, blank=True)
    apps = models.ArrayField(model_container=App)

class Customer(models.Model):
    _id = models.ObjectIdField()
    email = models.CharField(max_length=60, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    roles = models.ArrayField(model_container=Role)


class Message(models.Model):
    _id = models.ObjectIdField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
