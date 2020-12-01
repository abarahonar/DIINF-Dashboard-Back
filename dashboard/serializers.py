from rest_framework import serializers

from dashboard.models import App, Customer, Role


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ('_id', 'name', 'url')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('_id', 'name', 'apps')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['_id', 'username', 'email', 'first_name', 'last_name', 'roles']
