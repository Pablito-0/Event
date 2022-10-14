from rest_framework import serializers
from .models import *


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date', 'title')
        read_only_fields = ('id',)


    def create(self, validated_data):
        validated_data['ticket_count'] = validated_data.get('ticket_count', 15)
        return super().create(validated_data)


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ('price', 'number', 'vip')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('title',)

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
