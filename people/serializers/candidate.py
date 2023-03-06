from rest_framework import serializers
from people.models import Candidate
from .party import PartyAsChildSerializer
from poll.serializers import PositionSerializer


class CandidateSerializer(serializers.ModelSerializer):
    party = PartyAsChildSerializer()
    position = PositionSerializer()
    class Meta:
        model = Candidate
        fields = ('pk', 'full_name', 'party', 'position', 'description', 'status', 'created_at')
