from rest_framework import serializers
from geo.models import Nation


class NationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nation
        fields = ('pk', 'code', 'title', 'agent')
