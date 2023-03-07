from rest_framework import serializers
from geo.models import Nation
from people.models import Agent
from django.contrib.contenttypes.models import ContentType
from people.serializers import AgentSerializer


class NationSerializer(serializers.ModelSerializer):
    agent = serializers.SerializerMethodField()

    class Meta:
        model = Nation
        fields = ('pk', 'code', 'title', 'agent')

    def get_agent(self, obj):
        zone_ct = ContentType.objects.get_for_model(Nation)
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
