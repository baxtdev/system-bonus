from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import News
from .serializers import NewsSerializer
from api.view import StandardResultsSetPagination

class NewsViewSet(ReadOnlyModelViewSet):
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination
    queryset = News.objects.all().order_by('-id').filter(published=True)