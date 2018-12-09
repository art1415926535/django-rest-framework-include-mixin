# Django
from django.contrib.auth.models import Group, User

# Rest Framework
from rest_framework.viewsets import ReadOnlyModelViewSet

# Project apps
from rest_framework_include_mixin import QueryOptimizerMixin

# This app
from .models import UserProfile
from .serializers import GroupSerializer, ProfileSerializer, UserSerializer


class UserViewSet(QueryOptimizerMixin, ReadOnlyModelViewSet):
    """
    Users.

    list:
    Available includable objects:

      * groups - user groups.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    select_related = {
        'profile': 'userprofile',
    }
    prefetch_related = {
        'groups': 'groups',
        'may_know_users': 'groups__user_set',
    }


class ProfileViewSet(QueryOptimizerMixin, ReadOnlyModelViewSet):
    """
    User profiles.

    list:
    Available includable objects:

      * user - django user.
    """
    lookup_field = 'user'
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    select_related = {
        'user': 'user',
    }


class GroupViewSet(QueryOptimizerMixin, ReadOnlyModelViewSet):
    """
    Groups.

    list:
    Available includable objects:

      * users - all users;
      * active_users - only active users.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # Example:
    # prefetch_related = {
    #     'users': 'user_set',
    #     'active_users': Prefetch(
    #         lookup='user_set',
    #         queryset=User.objects.filter(is_active=True),
    #         to_attr='active_users',
    #     ),
    # }
