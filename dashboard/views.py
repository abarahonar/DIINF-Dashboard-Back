import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dashboard.models import App, Role, Customer
from dashboard.serializers import AppSerializer, RoleSerializer


def create(request):
    app = App.objects.get(name='App 2', url='url2')
    s = AppSerializer(app)
    role = Role.objects.get(name='Rol 1')
    apps = role.apps
    apps.append(s.data)
    role.apps = apps
    role.save()
    return

@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def list_apps(request):
    if not App.objects.all():
        create_dummys()
    apps = App.objects.all()
    serialized_apps = AppSerializer(apps, many=True)
    return JsonResponse(serialized_apps.data, safe=False)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def apps_by_user(request):
    if not Customer.objects.all():
        create_dummys()

    # useremail = request.GET.get('email',None)
    useremail = 'javiera.ayala.usach.cl'
    if useremail is not None:
        try:
            user = Customer.objects.get(email=useremail)
        except User.DoesNotExist:
            pass
        user_apps = user.roles[0]['apps']
        for apps in user_apps:
            apps['_id'] = str(apps['_id'])
        return JsonResponse(user_apps, safe=False)


def create_dummys():
    if not App.objects.all():
        app1 = App.objects.create(name='App 1', url='url1')
        app2 = App.objects.create(name='App 2', url='url2')

        s1 = AppSerializer(app1)
        s2 = AppSerializer(app2)

        role, created = Role.objects.get_or_create(name='Rol 1')

        #apps = role.apps
        # apps.append(s.data)
        #role.apps = apps

        role.apps = [s1.data, s2.data]
        role.save()
    if not Customer.objects.all():
        user = Customer.objects.create(username='JavieraAyala01', email='javiera.ayala.usach.cl', first_name='Javiera',
                                    last_name='Ayala')
        role = Role.objects.get(name='Rol 1')
        print(role.apps)
        serialized_role = RoleSerializer(role)
        print(serialized_role.data)
        user.roles = [serialized_role.data]
        print('no')
        user.save()


    return