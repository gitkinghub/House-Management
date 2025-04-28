from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User


from .permissions import IsHouseManagerOrNone

from .serializers import HouseSerializer

from .models import House

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHouseManagerOrNone, ]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['members']

    @action(detail=True, methods=['post'], name='join', permission_classes=[])
    def join(self, request, pk=None): #pk is for the model that has called this function
        try:
            house = self.get_object()
            user_profile = request.user.profile

            if user_profile.house == None:
                user_profile.house = house
                user_profile.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            elif user_profile in house.members.all():
                return Response({"detail": "You have already joined this house"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You are already in another house"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["post"], name="leave", permission_classes=[])
    def leave(self, request, pk=None): #pk is for the model that has called this function
        try:
            house = self.get_object()
            user_profile = request.user.profile

            if user_profile in house.members.all():
                user_profile.house = None
                user_profile.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You are not in this house"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=["post"], permission_classes=[], name="Remove Member")
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get("user_id", None)

            if user_id == None:
                return Response({'user_id': "User ID is Not Provided"}, status=status.HTTP_400_BAD_REQUEST)
    
            user_profile = User.objects.get(pk=user_id).profile
            house_members = house.members
            if user_profile in house_members.all():
                house_members.remove(user_profile)
                house.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "User is not in this house"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Provided user id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
