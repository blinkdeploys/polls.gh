from rest_framework import serializers
from people.models import Party


class PartySerializer(serializers.ModelSerializer):
    # votes = serializers.SerializerMethodField()
    # candidates = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = ('pk', 'code', 'title', 'details',
                  'total_candidates',
                  'candidates',
                  'votes',
                  'agent', 'status', 'created_at')

    # def get_votes(self, obj):
    #     total_votes = 0
    #     result_sets = [p.result_set for p in obj.candidate_set.prefetch_related('result_set').all()]
    #     for result_set in result_sets:
    #         for result in result_set:
    #             total_votes = total_votes + result.total_votes
    #     return sum(total_votes)

    # def get_candidates(self, obj):
    #     return obj.candidate_set.all()
