from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckViewTests(APITestCase):
    def test_health_check_returns_ok(self):
        url = reverse('health-check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'ok'})

    def test_health_check_rejects_post(self):
        url = reverse('health-check')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SchemaEndpointTests(TestCase):
    def test_schema_endpoint_returns_200(self):
        response = self.client.get('/api/schema/')

        self.assertEqual(response.status_code, 200)

    def test_swagger_ui_returns_200(self):
        response = self.client.get('/api/docs/')

        self.assertEqual(response.status_code, 200)
