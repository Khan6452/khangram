from rest_framework import serializers
from . import models
from khangram.users import serializers as user_serializers
from khangram.images import serializers as iamge_serializers

class NotificationSerializer(serializers.ModelSerializer):

    creator = user_serializers.ListUserSerializer()
    image = iamge_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notification
        fields = '__all__'