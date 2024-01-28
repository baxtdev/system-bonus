
from .models import News
from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField


class NewsSerializer(serializers.ModelSerializer):
    author__full_name = serializers.CharField(source='author.get_full_name', read_only=True)

    thumbnail = HyperlinkedSorlImageField(
        '128x128',
        options={"crop": "center"},
        source='image',
        read_only=True
    )

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'thumbnail', 'description', 'created_at', 'edited_at', 'seo_title', 'seo_description', 'author__full_name']