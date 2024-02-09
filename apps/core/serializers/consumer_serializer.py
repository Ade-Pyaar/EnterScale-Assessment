from rest_framework import serializers

from customer.models import Consumer


class ConsumerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["id", "email", "phone_number"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return data


class ConsumerSerializer:

    @staticmethod
    def get_all_consumer():
        consumers = Consumer.objects.all()

        data = ConsumerDetailsSerializer(consumers, many=True).data

        return data
