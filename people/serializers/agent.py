from rest_framework import serializers
from people.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('pk', 'full_name', 'zone', 'zone_title', 'zone_type', 'email', 'phone', 'address', 'zone_ct', 'zone_id', 'status', 'created_at')
