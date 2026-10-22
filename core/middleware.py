"""
Security hardening middleware for Campus Gabaa.
Defends against automated scanning, brute-force attacks, and DoS probes
from campus network environments.
"""
import time
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden


class SecurityHardeningMiddleware:
    """
    Protects login endpoints and sensitive URLs with in-memory throttling,
    blocks malicious scanner probes, and enforces strict security headers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # Suspicious paths typically scanned by automated penetration tools
        self.blocked_probe_prefixes = (
            '/.env',
            '/.git',
            '/wp-',
            '/phpmyadmin',
            '/shell',
            '/boaform',
            '/cgi-bin',
            '/.aws',
            '/.ssh',
        )

    def __call__(self, request):
        path = request.path.lower()
        ip = self.get_client_ip(request)

        # 1. Block common vulnerability scanner probes immediately
        for prefix in self.blocked_probe_prefixes:
            if path.startswith(prefix) or prefix in path:
                return HttpResponseForbidden("Access Denied: Security violation detected.")

        if '..' in path:
            return HttpResponseForbidden("Access Denied: Path traversal detected.")

        # 2. Login endpoint rate-limiting (Anti Brute-Force)
        if path == '/accounts/login/' and request.method == 'POST':
            login_key = f"rl:login:{ip}"
            attempts = cache.get(login_key, 0)
            if attempts >= 8:
                return HttpResponse(
                    "<h3>429 Too Many Requests</h3>"
                    "<p>Too many login attempts detected from your network address. "
                    "For security reasons, your IP is temporarily throttled. "
                    "Please wait 10 minutes or contact HU Campus Operations.</p>",
                    status=429
                )
            cache.set(login_key, attempts + 1, timeout=300)

        # 3. Aggressive scraper / DoS throttling (120 req/min per IP)
        throttle_key = f"rl:rate:{ip}:{int(time.time() // 60)}"
        request_count = cache.get(throttle_key, 0)
        if request_count > 150:
            return HttpResponse(
                "<h3>429 Too Many Requests</h3>"
                "<p>Rate limit exceeded. Please slow down your requests.</p>",
                status=429
            )
        cache.set(throttle_key, request_count + 1, timeout=65)

        response = self.get_response(request)

        # 4. Strict defense-in-depth security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
