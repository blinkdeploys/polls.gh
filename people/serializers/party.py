from rest_framework import serializers
from people.models import Party


class PartySerializer(serializers.ModelSerializer):
    # result_votes = serializers.SerializerMethodField()
    # candidates = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = ('pk', 'code', 'title', 'details',
                  'total_candidates',
                  'candidates',
                  'result_votes',
                  'agent', 'status', 'created_at')

    # def get_candidates(self, obj):
    #     return obj.candidate_set.all()
