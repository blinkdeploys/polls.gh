from rest_framework import serializers
from people.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('pk', 'title', 'details', 'office', 'position', 'start', 'end', 'status', 'created_at')
