from rest_framework import serializers
from geo.models import Region
from geo.serializers import NationSerializer


class RegionSerializer(serializers.ModelSerializer):
    nation = NationSerializer()
    class Meta:
        model = Region
        fields = ('pk', 'title', 'details', 'nation', 'status', 'agent', 'created_at')
