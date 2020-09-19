from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import os
def home(request):
	if 'id' not in request.session:
		return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/chat/')

def chat(request, receiver_name=None):
	if 'id' not in request.session:
		return HttpResponseRedirect('/login/')

	if receiver_name is not None:
		return render(request, 'chat-2.html', {
			'receiver_id': User.objects.filter(username=receiver_name).first().id,
			'user_id': request.session.get('id'), 
			'receiver_name': User.objects.filter(username=receiver_name).first().first_name +' '+ User.objects.filter(username=receiver_name).first().last_name,
			'name': User.objects.filter(id=request.session.get('id')).first().first_name + ' ' + User.objects.filter(id=request.session.get('id')).first().last_name
			 })
	else:
		return render(request, 'chat-2.html', {
			'name': User.objects.filter(id=request.session.get('id')).first().first_name + ' ' + User.objects.filter(id=request.session.get('id')).first().last_name,
			'user_id': request.session.get('id')			
			})

def login(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = User.objects.filter(username=username, password=password).first()
		if user is not None:
			request.session['id'] = user.id


		return HttpResponseRedirect('/chat/')
	return render(request, 'login.html')

def show_username(request):
	return HttpResponse(request.session.get('id', 'FAILED TO LOAD SESSIONS DATA'))


def signup(request):
	if request.POST:
		username = request.POST.get('username')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		photo = request.FILES['photo']
		

		user = User(username=username, first_name=first_name, last_name=last_name, password=password, photo=photo)
		user.save()

		name, extension = os.path.splitext(user.photo.path)

		os.rename(user.photo.path, os.path.dirname(user.photo.path)+ '/' + str(user.id))
		print(user.photo.path, ' ------ ', os.path.dirname(user.photo.path), '-------', user.id)
		user.photo.name = 'users/'+str(user.id)
		user.save()



		
		# return HttpResponse('User created successfully with photo: '+user.photo.name)

		return HttpResponseRedirect('/login/')



	return render(request, 'signup.html')