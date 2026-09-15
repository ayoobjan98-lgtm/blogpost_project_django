from django.http import HttpResponseForbidden

from django.shortcuts import render

class APIAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/api/"):
            if not request.user.is_authenticated:
                return render(request, "403.html", status=404)

            if not request.user.is_staff:
                return render(request, "403.html", status=404)

        return self.get_response(request)