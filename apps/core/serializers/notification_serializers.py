from rest_framework import serializers

from core.models import Notification


class NotificationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "title", "notification_type", "body"]


class NotificationSerializer:

    @staticmethod
    def get_all_notifications():

        notifications = Notification.objects.all()

        data = NotificationDetailsSerializer(notifications, many=True).data

        return data
