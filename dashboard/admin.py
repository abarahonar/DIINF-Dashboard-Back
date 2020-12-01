from django.contrib import admin

# Register your models here.
from dashboard.models import App, Role

admin.site.register(App)
admin.site.register(Role)
