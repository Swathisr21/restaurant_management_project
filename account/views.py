# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserProfileUpdateSerializer
from django.contrib.auth import logout

def logout_view(request):
    """Simple logout view that works with GET requests"""
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


class UserProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user = request.user

        serializer = UserProfileUpdateSerializer(
            user,
            data=request.data,
            partial=False
        )

        if serializer.is_valid():
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
