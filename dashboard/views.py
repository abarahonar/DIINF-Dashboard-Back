import json
import ssl
import urllib.request
from urllib.error import HTTPError

from bson import ObjectId
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from dashboard.models import App, Role, Customer, Message
from dashboard.serializers import AppSerializer, RoleSerializer
HEADERS = {'Content-Type': 'application/json'}
CONTEXT = ssl._create_unverified_context()


@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def edit_welcome_message(request):
    message = request.POST.get('message', None)
    if message is not None:
        Message.objects.create(message=message, status='Alive')
    return JsonResponse({}, status=HTTP_200_OK, safe=False)


# Inputs: role_name
@api_view(['GET'])
def get_last_message(request):
    message = Message.objects.filter(status='Alive').last()
    return JsonResponse({'message': message.message}, status=HTTP_200_OK)


# Inputs: role_name
@api_view(['POST'])
def create_role(request):
    role_name = request.POST['role_name']
    Role.objects.create(name=role_name, apps=[])
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
    app_name = request.POST['app_name']
    app_url = request.POST['app_url']
    img_url = request.POST['img']
    App.objects.create(name=app_name, url=app_url, img=img_url)
    return JsonResponse({}, status=HTTP_200_OK)


# Inputs: app id 'id'
@api_view(['POST'])
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
    new_img_url = request.POST.get('img', None)
    if new_app_name is not None and new_app_name != '':
        app.name = new_app_name
    if new_app_url is not None and new_app_url != '':
        app.url = new_app_url
    if new_img_url is not None and new_img_url != '':
        app.img = new_img_url
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
    if not Role.objects.all():
        create_dummys()
    roles = Role.objects.all()
    serialized_roles = RoleSerializer(roles, many=True)
    print(serialized_roles.data)
    return JsonResponse(serialized_roles.data, safe=False)


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
    if token is None:
        return JsonResponse({'res': 'Cookie not found'}, status=500)
    # token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InRCME0yQSJ9.eyJpc3MiOiJodHRwczovL3Nlc3Npb24uZmlyZWJhc2UuZ29vZ2xlLmNvbS90aW5nZXNvLTU1ODgwIiwibmFtZSI6ImtldmluIHZpbGxhbG9ib3Mgc29yaWFubyIsInBpY3R1cmUiOiJodHRwczovL2xoNS5nb29nbGV1c2VyY29udGVudC5jb20vLUlSdzdJMWdfM0ZzL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FNWnV1Y25TdWNjOW5PWDBMOTZhelc4NGRkdldSejltTEEvczk2LWMvcGhvdG8uanBnIiwiYXVkIjoidGluZ2Vzby01NTg4MCIsImF1dGhfdGltZSI6MTYxNDYzMjcwNSwidXNlcl9pZCI6ImFWbkNlREtLeUloMWdPc2tmMzNQSHRackM1bzIiLCJzdWIiOiJhVm5DZURLS3lJaDFnT3NrZjMzUEh0WnJDNW8yIiwiaWF0IjoxNjE0NjMyNzA4LCJleHAiOjE2MTUwNjQ3MDgsImVtYWlsIjoia2V2aW4udmlsbGFsb2Jvc0B1c2FjaC5jbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE3MzgwOTU0NDc0NTkyMzM0NDIwIl0sImVtYWlsIjpbImtldmluLnZpbGxhbG9ib3NAdXNhY2guY2wiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.NIafkU2R5iFEvynKKt7iBVlV4NsYk5VUay9TF0Tf8o2ORux_1lxH_54NyeVS5CWhCM7y9CD5fCDwvG1dJrmn1oGO_rc3nJwsNzitx7CDBb_ax2Mducs2slEKw386cLOu_7aO_xw55x1YgBd61cFGl6dytUvVdueWbFQhC8KYJWyGOvqN3lGWSuvkMUPSlxRTRcza2j0X9uRUSx7PX-LpO1j23-k6GbtnLc5EbfLFOTJJnrr9RbRGuF1LuhSQDNWBGtViKoT63BObV05_WrgK2POzqDlXvbtUgjRFCyn4555Y-eH1hhxI60ClNsmFv8eHjgtAQJGPp25-K0SQP5-JuQ'

    payload = json.dumps({'idToken': token}).encode("utf-8")
    req = urllib.request.Request('https://back.catteam.tk/authorize', payload, HEADERS)
    try:
        with urllib.request.urlopen(req, context=CONTEXT) as f:
            response = f.read()
    except HTTPError:
        return JsonResponse({'res': 'Usuario no encontrado'}, status=401)
    json_data = response.decode()
    user_roles = json.loads(json_data)['result']
    roles = Role.objects.filter(name__in=user_roles)
    if not roles:
        pass
    serialized_apps = RoleSerializer(roles, many=True)
    return JsonResponse({'res': serialized_apps.data}, safe=False)


def create_dummy_roles(role_name):
    if role_name == 'Alumno':
        app1, _ = App.objects.get_or_create(name='Facebook', url='https://www.facebook.com',
                                            img='https://www.facebook.com/images/fb_icon_325x325.png')
        app2, _ = App.objects.get_or_create(name='Google', url='https://www.google.com',
                                            img='https://elegirhoy.com/uploads/fichas-eventos-imagenes/la-fundacion-de-google.png')
    else:
        app1, _ = App.objects.get_or_create(name='Youtube', url='https://www.youtube.com',
                                            img='https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc')
        app2, _ = App.objects.get_or_create(name='Twitter', url='https://www.twitter.com',
                                            img='https://play-lh.googleusercontent.com/J8k5q78xv4R8Smi4vOE6iUphLvOz0efC-0lzoyGfd0KRUlAv4ekuCtlss6KBN-tMvEw')

    s1 = AppSerializer(app1)
    s2 = AppSerializer(app2)

    role = Role.objects.create(name=role_name)
    role.apps = [s1.data, s2.data]
    role.save()
    return role


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
        serialized_role = RoleSerializer(role)
        user.roles = [serialized_role.data]
        user.save()


    return