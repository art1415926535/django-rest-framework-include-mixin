# Third Party
from model_mommy import mommy

# Django
from django.contrib.auth.models import Group, User
from django.test import TransactionTestCase

# Rest Framework
from rest_framework import status
from rest_framework.test import APIClient

# Project apps
from tests.models import UserProfile


class TestViews(TransactionTestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        super(TestViews, cls).setUpClass()

        cls.number = 3
        mommy.make(UserProfile, _quantity=cls.number)
        mommy.make(Group, _quantity=cls.number)
        for user in User.objects.all():
            for group in Group.objects.all():
                user.groups.add(group)

    def test_select(self):
        with self.assertNumQueries(1):
            response = self.client.get(
                '/users/',
                data=[
                    ('include[]', 'profile'),
                ],
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            self.number,
        )

        self.assertSetEqual(
            set(response.data[0].keys()),
            {'id', 'first_name', 'last_name', 'username', 'profile'},
        )

    def test_prefetch(self):
        with self.assertNumQueries(3):
            response = self.client.get(
                '/users/',
                data=[
                    ('include[]', 'groups'),
                    ('include[]', 'may_know_users'),
                ],
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            self.number,
        )

        self.assertSetEqual(
            set(response.data[0].keys()),
            {'id', 'first_name', 'last_name', 'username',
             'groups', 'may_know_users'},
        )

    def test_without_select_related_and_prefetch_related(self):
        response = self.client.get('/groups/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
