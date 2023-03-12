from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices, NameTitleChoices
from geo.models import Nation, Constituency
from poll.models import Result, Position, ResultSheet
from django.contrib.contenttypes.models import ContentType


class Candidate(models.Model):
    prefix = models.CharField(_("Candidate title"), max_length=255, blank=True, null=True)
    first_name = models.CharField(_("Candidate first name"), max_length=255, default='')
    last_name = models.CharField(_("Candidate last name"), max_length=255, default='')
    other_names = models.CharField(_("Candidate other names"), max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    party = models.ForeignKey(
        "people.Party",
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='candidates'
    )
    position = models.ForeignKey(
        "poll.Position",
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='candidates'
    )
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    
    class Meta:
        db_table = 'people_candidate'

    def __str__(self):
        return "{} {} {} {} ({})".format(self.prefix, self.first_name, self.last_name, self.other_names, self.party.code)

    @property
    def full_name(self):
        return "{} {} {}".format(self.prefix, self.first_name, self.last_name)

    @property
    def votes(self) -> int:
        votes = 0
        results = self.results.all()
        for result in results:
            votes = votes + int(result.votes)
        return votes

    @property
    def won(self) -> bool:
        position = self.position
        print(position)
        position=Position.objects.filter(
            zone_ct=position.zone_ct,
            zone_id=position.zone_id
        ).first()
        if position.zone_ct == ContentType.objects.get_for_model(Nation):
            return True
        elif position.zone_ct == ContentType.objects.get_for_model(Constituency):
            # get the position the candiate applied for
            position = self.position
            # get all the results for this position
            result_sheets = ResultSheet.objects \
                                    .filter(position=position) \
                                    .prefetch_related('results') \
                                    .all()
            # if this candidates results has the most votes than it wins
            candidate_votes = {}
            winning_candidate = None
            max_votes = 0
            for result_sheet in result_sheets:
                for result in result_sheet.results.all():
                    total_votes = candidate_votes.get(result.candidate.pk, 0)
                    total_votes = total_votes + result.votes
                    candidate_votes[result.candidate.pk] = total_votes
                    if max_votes < total_votes:
                        winning_candidate = result.candidate
                        max_votes = total_votes
            if winning_candidate is not None:
                if winning_candidate.pk == self.pk:
                    return True
        return False

