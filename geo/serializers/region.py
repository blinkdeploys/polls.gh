from rest_framework import serializers
from geo.models import Region
from geo.serializers import NationSerializer
from people.models import Agent
from django.contrib.contenttypes.models import ContentType


class RegionSerializer(serializers.ModelSerializer):
    nation = NationSerializer()
    agent = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('pk', 'title', 'details', 'nation', 'agent', 'status', 'created_at')

    def get_agent(self, obj):
        zone_ct = ContentType.objects.get_for_model(Region)
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
