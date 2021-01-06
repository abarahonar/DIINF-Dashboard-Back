"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import dashboard.views as dash_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list-apps', dash_views.list_apps),
    path('list-roles', dash_views.list_roles),
    path('user-apps', dash_views.apps_by_user),
    path('create-app', dash_views.create_app),
    path('create-role', dash_views.create_role),
    path('add-app', dash_views.add_app_to_role),
    path('delete-app', dash_views.delete_app),
    path('delete-role', dash_views.delete_role),
    path('update-app', dash_views.update_app),
    path('create-message', dash_views.edit_welcome_message),
    path('get-message', dash_views.get_last_message)
    #path('edit-role', dash_views.delete_role),
]
