# -*- coding: utf-8 -*-
"""
This test file will verify proper password policy enforcement, which is an option feature
"""
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from mock import patch
from django.test.utils import override_settings


@patch.dict("django.conf.settings.FEATURES", {'ENFORCE_PASSWORD_POLICY': True})
class TestPasswordPolicy(TestCase):
    """
    Go through some password policy tests to make sure things are properly working
    """
    def setUp(self):
        super(TestPasswordPolicy, self).setUp()
        self.url = reverse('create_account')

        self.url_params = {
            'username': 'username',
            'email': 'foo_bar@bar.com',
            'name': 'username',
            'terms_of_service': 'true',
            'honor_code': 'true',
        }

    @override_settings(PASSWORD_MIN_LENGTH=6)
    def test_password_length_too_short(self):
        self.url_params['password'] = 'aaa'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Invalid Length (must be 6 characters or more)",
        )

    @override_settings(PASSWORD_MIN_LENGTH=6)
    def test_password_length_long_enough(self):
        self.url_params['password'] = 'ThisIsALongerPassword'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @override_settings(PASSWORD_MAX_LENGTH=12)
    def test_password_length_too_long(self):
        self.url_params['password'] = 'ThisPasswordIsWayTooLong'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Invalid Length (must be 12 characters or less)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'UPPER': 3})
    def test_password_not_enough_uppercase(self):
        self.url_params['password'] = 'thisshouldfail'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Must be more complex (must contain 3 or more uppercase characters)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'UPPER': 3})
    def test_password_enough_uppercase(self):
        self.url_params['password'] = 'ThisShouldPass'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'LOWER': 3})
    def test_password_not_enough_lowercase(self):
        self.url_params['password'] = 'THISSHOULDFAIL'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Must be more complex (must contain 3 or more lowercase characters)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'LOWER': 3})
    def test_password_enough_lowercase(self):
        self.url_params['password'] = 'ThisShouldPass'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'DIGITS': 3})
    def test_not_enough_digits(self):
        self.url_params['password'] = 'thishasnodigits'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Must be more complex (must contain 3 or more digits)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'DIGITS': 3})
    def test_enough_digits(self):
        self.url_params['password'] = 'Th1sSh0uldPa88'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'PUNCTUATION': 3})
    def test_not_enough_punctuations(self):
        self.url_params['password'] = 'thisshouldfail'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Must be more complex (must contain 3 or more punctuation characters)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'PUNCTUATION': 3})
    def test_enough_punctuations(self):
        self.url_params['password'] = 'Th!sSh.uldPa$*'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'WORDS': 3})
    def test_not_enough_words(self):
        self.url_params['password'] = 'thisshouldfail'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Must be more complex (must contain 3 or more unique words)",
        )

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {'WORDS': 3})
    def test_enough_wordss(self):
        self.url_params['password'] = u'this should pass'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {
        'PUNCTUATION': 3,
        'WORDS': 3,
        'DIGITS': 3,
        'LOWER': 3,
        'UPPER': 3,
    })
    def test_multiple_errors_fail(self):
        self.url_params['password'] = 'thisshouldfail'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        errstring = ("Password: Must be more complex ("
            "must contain 3 or more uppercase characters, "
            "must contain 3 or more digits, "
            "must contain 3 or more punctuation characters, "
            "must contain 3 or more unique words"
            ")")
        self.assertEqual(obj['value'], errstring)

    @patch.dict("django.conf.settings.PASSWORD_COMPLEXITY", {
        'PUNCTUATION': 3,
        'WORDS': 3,
        'DIGITS': 3,
        'LOWER': 3,
        'UPPER': 3,
    })
    def test_multiple_errors_pass(self):
        self.url_params['password'] = u'tH1s Sh0u!d P3#$'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @override_settings(PASSWORD_DICTIONARY=['foo', 'bar'])
    @override_settings(PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD=1)
    def test_dictionary_similarity_fail1(self):
        self.url_params['password'] = 'foo'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Too similar to a restricted dictionary word.",
        )

    @override_settings(PASSWORD_DICTIONARY=['foo', 'bar'])
    @override_settings(PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD=1)
    def test_dictionary_similarity_fail2(self):
        self.url_params['password'] = 'bar'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Too similar to a restricted dictionary word.",
        )

    @override_settings(PASSWORD_DICTIONARY=['foo', 'bar'])
    @override_settings(PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD=1)
    def test_dictionary_similarity_fail3(self):
        self.url_params['password'] = 'fo0'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            "Password: Too similar to a restricted dictionary word.",
        )

    @override_settings(PASSWORD_DICTIONARY=['foo', 'bar'])
    @override_settings(PASSWORD_DICTIONARY_EDIT_DISTANCE_THRESHOLD=1)
    def test_dictionary_similarity_pass(self):
        self.url_params['password'] = 'this_is_ok'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    def test_with_unicode(self):
        self.url_params['password'] = u'四節比分和七年前'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])
