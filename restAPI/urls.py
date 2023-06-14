from django.urls import include, path
from rest_framework import routers
from restAPI.APIApp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'states', views.StateViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('populate_database', views.populate_database),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
