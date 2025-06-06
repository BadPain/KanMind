from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import CustomUser as User


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        repeated_password = data.get('repeated_password')

        if not fullname or not email or not password or not repeated_password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if password != repeated_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=fullname
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "fullname": user.first_name,
            "email": user.email,
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "fullname": user.first_name,
            "email": user.email,
            "user_id": user.id
        }, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            return Response({
                "id": user.id,
                "email": user.email,
                "fullname": user.first_name,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)
