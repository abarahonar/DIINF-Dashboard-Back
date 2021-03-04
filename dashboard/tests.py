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
        self.assertEqual(response.status_code, 500)

# Authorization Test
# Its successful if accepts an incoming request from XHRR
class RoleListTest(TestCase):

    def test(self):
        req = RequestFactory().get('/list-roles')
        response = views.list_roles(req)
        self.assertEqual(response.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHRR
class CreateApp(TestCase):

    def test(self):
        req = RequestFactory().post('/create-role', {'app_name': 'App 1', 'app_url': 'url 1', 'app_img': 'url_to_img'})
        response = views.create_app(req)
        self.assertEqual(response.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHR
class CreateRole(TestCase):

    def test(self):
        req = RequestFactory().post('/create-role', {'role_name': 'Rol 1'})
        response = views.create_role(req)
        self.assertEqual(response.status_code, 200)


# Add app to role Test
# Its successful if the system can add an app to a role
class AddAppToRole(TestCase):

    def test(self):
        # New App
        new_app = RequestFactory().post('/create-app', {'app_name': 'App 1', 'app_url': 'url 1', 'app_img': 'url_to_img'})
        # New Role
        new_role = RequestFactory().post('/create-role', {'role_name': 'Rol 1'})
        # Create the new elements
        views.create_app(new_app)
        views.create_role(new_role)
        # Get the role using a query
        role = Role.objects.get(name='Rol 1')
        # get the app using a query
        app = App.objects.get(name='App 1', url='url 1')
        # Testing the endpoint
        new_role = RequestFactory().post('/add-app', {'app_id': app.pk, 'role_id': role.pk})
        final = views.add_app_to_role(new_role)
        self.assertEqual(final.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHRR
class UpdateApp(TestCase):

    def test(self):
        create_app = RequestFactory().post('/create-app', {'app_name': 'App 1', 'app_url': 'url 1', 'app_img': 'url_to_img'})
        response = views.create_app(create_app)
        app = App.objects.get(name='App 1', url='url 1')
        new_app = RequestFactory().post('/create-role', {'id': app.pk, 'app_name': 'App 2', 'app_url': 'url 2'})
        final = views.update_app(new_app)
        self.assertEqual(final.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHRR
class DeleteApp(TestCase):

    def test(self):
        create_app =  RequestFactory().post('/create-app', {'app_name': 'App 1', 'app_url': 'url 1', 'app_img': 'url_to_img'})
        response = views.create_app(create_app)
        app = App.objects.get(name='App 1', url='url 1')
        new_app = RequestFactory().post('/create-role', {'id': app.pk})
        final = views.delete_app(new_app)
        self.assertEqual(final.status_code, 200)


# Authorization Test
# Its successful if accepts an incoming request from XHRR
class DeleteRole(TestCase):

    def test(self):
        create_app = RequestFactory().post('/create-role', {'role_name': 'Rol X'})
        views.create_role(create_app)
        role = Role.objects.get(name='Rol X')
        delete_role = RequestFactory().post('/delete-role', {'id': role.pk})
        final = views.delete_role(delete_role)
        self.assertEqual(final.status_code, 200)


