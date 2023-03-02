from rest_framework import serializers
from poll.models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('pk', 'title', 'zone')
