from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

class Notifications(APIView):

    def get(self, request, format=None):

        user = request.user

        notifications = models.Notification.objects.filter(to=user)

        serializer = serializers.NotificationSerializer(
            notifications, many=True
        )

        return Response(data=serializer.data, status=200)


def create_notification(creator, to, notification_type, image=None, comment=None):

    print(creator, to, notification_type, image, comment)

    notification = models.Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
        image=image,
        comment=comment
    )

    notification.save()