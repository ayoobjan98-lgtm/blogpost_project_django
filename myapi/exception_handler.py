from django.shortcuts import render
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 403:
            request = context["request"]

            return render(
                request,
                "403.html",
                status=403
            )

    return response