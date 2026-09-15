from django.shortcuts import get_object_or_404, render

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse

from .serializers import BlogPostSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from .permissions import IsAuthenticated


from project.accounts.models import User
from project.blogpost.models import BlogPost

import json

class BlogPostAPIView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    

class BlogPostDetailAPIView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]


class RegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.save()

            return render(
                request,
                "auth/login.html",
                {
                    "message": "ثبت نام با موفقیت انجام شد."
                }
            )

        return render(
            request,
            "auth/register.html",
            {
                "errors": serializer.errors
            },
            status=400
        )

    
class LoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            # فعلاً بعداً اینجا session/JWT را اضافه می‌کنیم

            return Response({
                "message": "ورود موفقیت‌آمیز بود.",
                "username": user.username,
            })

        return Response(
            {
                "errors": serializer.errors
            },
            status=400
        )

class UserInfoLogin(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    