# Django
from django.contrib.auth.models import Group, User
from django.utils.decorators import classproperty

# Rest Framework
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

# Project apps
from rest_framework_include_mixin import SerializerIncludeMixin
from tests.models import UserProfile


class GroupSerializer(SerializerIncludeMixin, ModelSerializer):
    @classproperty
    def extra_objects(cls):
        return {
            'users': UserSerializer(source='user_set', many=True),
            'active_users': UserSerializer(many=True),
        }

    class Meta:
        model = Group
        fields = ('name',)


class ProfileSerializer(SerializerIncludeMixin, ModelSerializer):
    @classproperty
    def extra_objects(cls):
        return {
            'user': UserSerializer(),
        }

    class Meta:
        model = UserProfile
        fields = ('user_id', 'bio')


class UserSerializer(SerializerIncludeMixin, ModelSerializer):
    @classproperty
    def extra_objects(cls):
        return {
            'groups': GroupSerializer(many=True),
            'profile': ProfileSerializer(source='userprofile'),
            'may_know_users': SerializerMethodField(),
        }

    def get_may_know_users(self, obj):
        users = set()
        for group in obj.groups.all():
            users = users.union(set(group.user_set.all()))

        return self.__class__(users, many=True).data

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
