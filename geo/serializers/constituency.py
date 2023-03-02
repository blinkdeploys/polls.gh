from rest_framework import serializers
from geo.models import Constituency
from geo.serializers import RegionSerializer


class ConstituencySerializer(serializers.ModelSerializer):
    # serializers.SerializerMethodField()
    region = RegionSerializer()
    class Meta:
        model = Constituency
        fields = ('pk', 'title', 'region')
