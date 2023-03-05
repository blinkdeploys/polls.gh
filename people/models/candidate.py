from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices, NameTitleChoices

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
    def result_votes(self):
        votes = 0
        results = self.results.all()
        for result in results:
            votes = votes + int(result.votes)
        return votes
