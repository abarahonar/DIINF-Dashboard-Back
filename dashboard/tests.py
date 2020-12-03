from django.test import TestCase, RequestFactory

from dashboard.models import Role, Customer, App
from . import views


# List Apps endpoint test
# Its successful if the list_apps method returns status 200
class ListAppsTest(TestCase):

    def test(self):
        req = RequestFactory().get('/list-apps')
        response = views.list_apps(req)
        self.assertEqual(response.status_code, 200)


# List User Apps endpoint test
# Its successful if the apps_by_user method returns status 200
class ListUserAppsTest(TestCase):

    def test(self):
        req = RequestFactory().get('/user-apps')
        response = views.apps_by_user(req)
        self.assertEqual(response.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHRR
class RoleListTest(TestCase):

    def test(self):
        req = RequestFactory().get('/list-roles')
        response = views.list_roles(req)
        self.assertEqual(response.status_code, 200)

