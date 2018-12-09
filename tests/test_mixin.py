# Django
from django.test import RequestFactory, TestCase

# Project apps
from rest_framework_include_mixin.mixins import IncludeMixin


class TestMixin(TestCase):
    def test_request_is_none(self):
        mixin = IncludeMixin()
        self.assertEqual(len(mixin.include_fields(None)), 0)

    def test_get_params(self):
        request = RequestFactory()
        request = request.get('/users/?include[]=groups&include[]=profile')

        mixin = IncludeMixin()
        self.assertSetEqual(
            set(mixin.include_fields(request)),
            {'groups', 'profile'},
        )
