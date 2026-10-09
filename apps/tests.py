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


class ProductionDefaultsTests(TestCase):
    def test_debug_is_off_when_env_missing(self):
        """Lokal .env bo'lmagan nusxada DEBUG standart holda False bo'lishi kerak."""
        import os
        import shutil
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        copy = Path(tempfile.mkdtemp()) / 'project'
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.env', '.git', '*.sqlite3'))
        env = {k: v for k, v in os.environ.items() if k not in ('DEBUG', 'ALLOWED_HOSTS')}
        env.update(SECRET_KEY='x' * 50, DJANGO_SETTINGS_MODULE='apitemplate.settings')
        code = "from django.conf import settings as s; print(s.DEBUG, s.ALLOWED_HOSTS)"
        result = subprocess.run([sys.executable, '-c', code], cwd=copy, env=env, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "False ['localhost', '127.0.0.1']", result.stderr)
