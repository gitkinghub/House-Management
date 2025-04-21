from rest_framework import routers

from .views import HouseViewSet

app_name = 'house'  #the app_name should be the name of the application

router = routers.DefaultRouter()
router.register("houses", HouseViewSet)
