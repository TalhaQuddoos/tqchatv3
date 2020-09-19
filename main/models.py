from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	photo = models.FileField(upload_to='users')
	password = models.CharField(max_length=50)
	online = models.CharField(max_length=100)

	channel = models.CharField(max_length=100)

class Message(models.Model):
	author = models.IntegerField(default=0)
	receiver = models.IntegerField(default=0)
	msg = models.TextField()
	time = models.DateTimeField(auto_now_add=True)

	seen = models.BooleanField(default=False)

	