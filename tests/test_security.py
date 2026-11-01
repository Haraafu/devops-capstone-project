"""Security regression tests exercise real Flask responses."""
from unittest import TestCase
from service import app


class TestSecurity(TestCase):
    """Security headers and explicit CORS policy."""

    def setUp(self):
        self.client = app.test_client()

    def test_headers(self):
        """It should return Talisman security headers."""
        for path in ["/", "/health", "/does-not-exist"]:
            response = self.client.get(path)
            self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
            self.assertIn("default-src", response.headers.get("Content-Security-Policy", ""))
            self.assertEqual(
                response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin"
            )

    def test_allowed_origin(self):
        """It should permit the configured origin."""
        response = self.client.get("/accounts", headers={"Origin": "http://localhost:3000"})
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000"
        )
        self.assertNotIn("Access-Control-Allow-Credentials", response.headers)

    def test_blocked_origin(self):
        """It should omit CORS permission for untrusted origins."""
        response = self.client.get("/accounts", headers={"Origin": "https://untrusted.example"})
        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_preflight(self):
        """It should allow the supported update method and Content-Type header."""
        response = self.client.options(
            "/accounts/1",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "PUT",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("PUT", response.headers.get("Access-Control-Allow-Methods", ""))
        self.assertIn("Content-Type", response.headers.get("Access-Control-Allow-Headers", ""))

    def test_hsts_on_https(self):
        """It should send HSTS over HTTPS."""
        response = self.client.get("/health", base_url="https://localhost")
        self.assertIn("max-age=", response.headers.get("Strict-Transport-Security", ""))
