from rest_framework import serializers
from poll.models import Result, ResultApproval
from people.serializers import CandidateSerializer
from geo.serializers import StationSerializer


class ResultSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer()
    station = StationSerializer()
    class Meta:
        model = Result
        fields = ('pk', 'candidate_details', 'candidate', 'station', 'total_votes', 'result_sheet', 'constituency_agent')



class ResultApprovalSerializer(serializers.ModelSerializer):
    result = ResultSerializer()
    class Meta:
        model = ResultApproval
        fields = ('pk', 'result', 'status', 'approved_at', 'created_at', 'approving_agent')
