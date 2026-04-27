from django.test import TestCase

# Create your tests here.

from django.test import TestCase


class CorsTests(TestCase):
    def test_cors_headers(self):
        response = self.client.get('/api/data/', HTTP_ORIGIN='http://localhost:3000')
        self.assertEqual(response['Access-Control-Allow-Origin'], 'http://localhost:3000')
