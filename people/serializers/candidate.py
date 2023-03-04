from rest_framework import serializers
from people.models import Candidate
from .party import PartySerializer
from poll.serializers import PositionSerializer


class CandidateSerializer(serializers.ModelSerializer):
    party = PartySerializer()
    position = PositionSerializer()
    class Meta:
        model = Candidate
        fields = ('pk', 'full_name', 'description', 'votes', 'party', 'position', 'status', 'created_at')
