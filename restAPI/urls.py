from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from restAPI import settings
from restAPI.APIApp import views

router = routers.DefaultRouter()
# router.register(r'groups', views.GroupViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'states', views.StateViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'players', views.PlayerViewSet, basename='player')
router.register(r'scores', views.ScoreViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login', views.login),
    path('populate_database', views.populate_database),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
