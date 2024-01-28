from django.urls import path, include

from rest_framework import routers

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from .yasg import urlpatterns as doc_url
from .api import *

router = routers.DefaultRouter()
router.register('pharmacy', PharmacyViewSet)
router.register('manager', ManagerViewSet)
router.register('history', HistoryViewSet)
router.register('news', NewsViewSet)
router.register('category-news', CategoriesViewSet)
router.register('discount_items', DiscountItemsViewSet)
router.register('free_call', FreeCallViewSet)
router.register('devices', FCMDeviceAuthorizedViewSet,basename='devices')
router.register('notifications',NotificationVieSet,'Notifications')
router.register('pushes',NotificationListAPIView,basename='Pushes')


urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include('rest_registration.api.urls')),
    path('notifications/make-read/<int:id>/',MakeReadNotificationAPIView.as_view()),
]
urlpatterns+=doc_url