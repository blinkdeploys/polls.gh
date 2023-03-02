from rest_framework import serializers
from geo.models import Station
from geo.serializers import ConstituencySerializer


class StationSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer()
    class Meta:
        model = Station
        fields = ('pk', 'code', 'title', 'details', 'constituency', 'status', 'agent', 'created_at')
