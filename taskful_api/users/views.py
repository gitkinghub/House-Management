from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .models import Profile
from .permissions import IsProfileOwnerOrReadOnly, IsUserOwnerOrGetAndPostOnly
from .serializers import ProfileSerilizer, UserSerializer

class Userviewset(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewset(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsProfileOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerilizer
