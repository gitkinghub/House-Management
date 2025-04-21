from rest_framework import routers

from .views import ProfileViewset, Userviewset

app_name = 'users'  #the app_name should be the name of the application

router = routers.DefaultRouter()
router.register("users", Userviewset)
router.register("profiles", ProfileViewset)
