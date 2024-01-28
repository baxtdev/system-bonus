from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_registration.utils.responses import get_ok_response



from apps.apteka.models import Pharmacy, Manager, History, DiscountItems
from apps.news.models import News,Categories
from apps.free_call.models import FreeCall
from .serializers import *
from .permissions import IsOwner
from accounts.models import Notification


class PharmacyViewSet(ReadOnlyModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


class ManagerViewSet(ReadOnlyModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class HistoryViewSet(ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        queryset = History.objects.filter(customer=self.request.user)
        if queryset:
            return queryset
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "У вас пусто"})   


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class DiscountItemsViewSet(ReadOnlyModelViewSet):
    queryset = DiscountItems.objects.all()
    serializer_class = DiscountItemsSerializer


class FreeCallViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    http_method_names = ['post']
    queryset = FreeCall.objects.all()
    serializer_class = FreeCallSerializer


class NotificationVieSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAdminUser,)


class NotificationListAPIView(ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return  qs.filter(for_all = True).union(qs.filter(user=self.request.user))


class MakeReadNotificationAPIView(GenericAPIView):

    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return get_ok_response(('Уведомление прочитано'))