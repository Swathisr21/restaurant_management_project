from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import viewset
from rest_framework.response import response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserProfileUpdateSerializer


class UserProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user = request.user

        serializer = UserProfileUpdateSerializer(
            user,
            data=request.data,
            partial=False
        )

        if serializer.is_valid()
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        