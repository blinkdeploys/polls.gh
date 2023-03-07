from rest_framework import serializers
from geo.models import Station
from geo.serializers import ConstituencySerializer
from people.models import Agent
from django.contrib.contenttypes.models import ContentType


class StationSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer()
    agent = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ('pk', 'code', 'title', 'details', 'constituency', 'agent', 'status', 'created_at')

    def get_agent(self, obj):
        zone_ct = ContentType.objects.get_for_model(Station)
        agent = Agent.objects.filter(
						zone_ct=zone_ct,
						zone_id=obj.pk
					).first()
        return dict(
            pk=agent.pk,
            full_name=agent.full_name,
            email=agent.email,
            phone=agent.phone,
            address=agent.address,
        )
