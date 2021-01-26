import json
import urllib.request

# Necesario para conexiones inseguras
import ssl
CONTEXT = ssl._create_unverified_context()

# Necesario para conectarse al sistema
URL = "https://back.catteam.tk/authorize"
HEADERS = {'Content-Type': 'application/json'}


from bson import ObjectId
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from dashboard.models import App, Role, Customer, Message
from dashboard.serializers import AppSerializer, RoleSerializer


@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def edit_welcome_message(request):
    message = request.POST.get('message', None)
    if message is not None:
        Message.objects.create(message=message, status='Alive')
    return JsonResponse({}, safe=False)


# Inputs: role_name
@api_view(['GET'])
def get_last_message(request):
    message = Message.objects.filter(status='Alive').last()
    return JsonResponse({'message': message.message}, status=HTTP_200_OK)


# Inputs: role_name
@api_view(['POST'])
def create_role(request):
    role_name = request.POST['role_name']
    Role.objects.create(name=role_name)
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: app_id, role_id
@api_view(['POST'])
def add_app_to_role(request):
    app = App.objects.get(pk=ObjectId(request.POST['app_id'].strip()))
    s = AppSerializer(app)
    role = Role.objects.get(pk=ObjectId(request.POST['role_id'].strip()))
    if role.apps:
        apps = role.apps
    else:
        apps = []
    apps.append(s.data)
    role.apps = apps
    role.save()
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: id
def delete_role(request):
    Role.objects.get(pk=ObjectId(request.POST['id'].strip())).delete()
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: app_name, app_url
@api_view(['POST'])
def create_app(request):
    print(request.body)
    app_name = request.POST['app_name']
    app_url = request.POST['app_url']
    App.objects.create(name=app_name, url=app_url)
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: app id 'id'
def delete_app(request):
    roles = Role.objects.filter(apps={'_id': request.POST['id'].strip()})
    for role in roles:
        new_apps = []
        print(role.apps)
        for app in role.apps:
            if app['_id'] == ObjectId(request.POST['id'].strip()):
                continue
            new_apps.append(app)
        role.apps = new_apps
        role.save()
    App.objects.get(pk=ObjectId(request.POST['id'].strip())).delete()
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: id, app_name, app_url
@api_view(['POST'])
def update_app(request):
    app = App.objects.get(pk=ObjectId(request.POST['id'].strip()))
    new_app_name = request.POST.get('app_name', None)
    new_app_url = request.POST.get('app_url', None)
    if new_app_name is not None:
        app.name = new_app_name
    if new_app_url is not None:
        app.url = new_app_url
    app.save()
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: id, role_name
@api_view(['POST'])
def update_role(request):
    role = Role.objects.get(pk=ObjectId(request.POST['id'].strip()))
    new_role_name = request.POST.get('app_name', None)
    role.name = new_role_name
    role.save()
    return JsonResponse({}, status=HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def list_roles(request):
    """
    Funcion modificada, originalmente no estaba retornando un JSON valido, no pude lograr que el serializer de Role retorne un json valido, por 
    lo que creo un diccionario aca mismo y lo relleno. Unica forma que encontre de retornar un JSON valido. Por lo que pude averiguar, Python en general
    tiene problemas con convertir objetos y arreglos anidados a JSON. 
    """
    if not Role.objects.all():
        create_dummys()
    roles = Role.objects.all()

    # Creacion del diccionario
    json_data = []
    for role in roles:
        role_data = {'_id': str(role._id), 'name': role.name, 'apps': []}
        for app in role.apps:
            app_data = {
                '_id': str(app['_id']),
                'name': app['name'],
                'url': app['url']
            }
            role_data['apps'].append(app_data)
        json_data.append(role_data)

    return JsonResponse(json_data, safe=False)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def list_apps(request):
    if not App.objects.all():
        create_dummys()
    apps = App.objects.all()
    serialized_apps = AppSerializer(apps, many=True)
    return JsonResponse(serialized_apps.data, safe=False)


@api_view(['GET', 'POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def apps_by_user(request):
    token = request.COOKIES.get('DIINFAUTH2USERTOKEN', None)

    try:
        payload = json.dumps({'idToken': token}).encode("utf-8")
        req = urllib.request.Request(URL, payload, HEADERS)
        with urllib.request.urlopen(req, context=CONTEXT) as f:
            response = f.read()
        json_data = response.decode()
        data = json.loads(json_data)
    except Exception as e:
        print(e)
    roles = data['result']
    for role in roles:
        try:
            pass# hacer wea de query
        except Exception as e:
            print(e)
    return JsonResponse({'rol': roles})

#    useremail = 'javiera.ayala.usach.cl'
#    if useremail is not None:
#        try:
#            user = Customer.objects.get(email=useremail)
#        except Customer.DoesNotExist:
#            pass
#        user_apps = user.roles[0]['apps']
#        for apps in user_apps:
#            apps['_id'] = str(apps['_id'])
#        return JsonResponse(user_apps, safe=False)


def create_dummys():
    if not App.objects.all():
        app1 = App.objects.create(name='Google', url='//google.cl')
        app2 = App.objects.create(name='Facebook', url='//facebook.com')

        s1 = AppSerializer(app1)
        s2 = AppSerializer(app2)

        role, created = Role.objects.get_or_create(name='Alumno')

        role.apps = [s1.data, s2.data]
        role.save()
    return