from rest_framework import serializers
from geo.models import Constituency
from geo.serializers import RegionSerializer
from people.models import Agent
from django.contrib.contenttypes.models import ContentType


class ConstituencySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    agent = serializers.SerializerMethodField()

    class Meta:
        model = Constituency
        fields = ('pk', 'title', 'region', 'agent')

    def get_agent(self, obj):
        zone_ct = ContentType.objects.get_for_model(Constituency)
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

