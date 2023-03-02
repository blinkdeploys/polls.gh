from rest_framework import serializers
from poll.models import Office


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('pk', 'title', 'level')
