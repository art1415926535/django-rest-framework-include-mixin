# Django
from django.test import RequestFactory, TestCase

# Rest Framework
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer

# Project apps
from tests.serializers import (
    GroupSerializer, ProfileSerializer, UserSerializer
)


class TestSerializers(TestCase):
    def test_request_is_none(self):
        """Test serializer without request."""
        serializer = UserSerializer()

        fields = serializer.fields

        self.assertSetEqual(
            set(fields.keys()),
            {'id', 'first_name', 'last_name', 'username'},
        )

    def test_request_without_include(self):
        """Test serializer without request."""
        request = RequestFactory()
        request = request.get('/users/')
        serializer = UserSerializer(context={'request': request})

        fields = serializer.fields
        self.assertSetEqual(
            set(fields.keys()),
            {'id', 'first_name', 'last_name', 'username'},
        )

    def test_include_field_many_true(self):
        """Test field serializer with `many=True`."""
        request = RequestFactory()
        request = request.get('/users/?include[]=groups')
        serializer = UserSerializer(context={'request': request})

        fields = serializer.fields

        self.assertSetEqual(
            set(fields.keys()),
            {'id', 'first_name', 'last_name', 'username', 'groups'},
        )
        self.assertIsInstance(
            fields['groups'],
            ListSerializer,
        )
        self.assertIsInstance(
            fields['groups'].child,
            GroupSerializer,
        )

    def test_include_field_many_false(self):
        """Test field serializer with `many=False`."""
        request = RequestFactory()
        request = request.get('/users/?include[]=profile')
        serializer = UserSerializer(context={'request': request})

        fields = serializer.fields

        self.assertSetEqual(
            set(fields.keys()),
            {'id', 'first_name', 'last_name', 'username', 'profile'},
        )
        self.assertIsInstance(
            fields['profile'],
            ProfileSerializer,
        )

    def test_replace(self):
        """Test replace field field with another."""
        request = RequestFactory()
        request = request.get('/profiles/?include[]=user')
        serializer = ProfileSerializer(context={'request': request})

        fields = serializer.fields

        self.assertSetEqual(
            set(fields.keys()),
            {'user', 'bio'},
        )
        self.assertIsInstance(
            fields['user'],
            UserSerializer,
        )

    def test_self_nested(self):
        """Test self include."""
        request = RequestFactory()
        request = request.get('/users/?include[]=may_know_users')
        serializer = UserSerializer(context={'request': request})

        fields = serializer.fields

        self.assertIn(
            'may_know_users',
            fields.keys(),
        )

    def test_wrong_include(self):
        """Test wrong GET param."""
        request = RequestFactory()
        request = request.get('/users/?include[]=UNEXPECTED')
        serializer = UserSerializer(context={'request': request})

        with self.assertRaises(ValidationError):
            serializer.fields  # noqa
