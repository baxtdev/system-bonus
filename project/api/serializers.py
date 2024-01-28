from rest_framework import serializers

from apps.apteka.models import Pharmacy, Manager, History, DiscountItems
from apps.news.models import News,Categories
from apps.free_call.models import FreeCall
from accounts.models import Notification, User


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    customer_bonus = serializers.CharField(read_only=True)
    class Meta:
        model = History
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    news = NewsSerializer(
        many=True,
        read_only = True
    )
    class Meta:
        model = Categories
        fields = ('id','title','description','news')


class DiscountItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountItems
        fields = '__all__'


class FreeCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeCall
        read_only_fields = ('id', 'created_at', 'status', 'customer')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id', 'code', 'last_activity', 'bonus')
        fields = [
            "id",
            "first_name",
            "last_name",
            "last_login",
            "phone",
            "email",
            "code",
            "image",
            "sex",
            "birthday",
            "bonus",
        ]
        


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model =Notification
        fields = '__all__'