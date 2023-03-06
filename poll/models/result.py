from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import GeoLevelChoices, StatusChoices
from poll.utils import upload_directory_path


class ResultSheet(models.Model):
    station = models.ForeignKey(
                                "geo.Station",
                                on_delete=models.CASCADE,
                                help_text=_("Polling Station"),
                                related_name='result_sheets',
                                default=True, null=True, blank=True)
    position = models.ForeignKey(
                                "poll.Position",
                                on_delete=models.CASCADE,
                                help_text=_("Position"),
                                related_name='result_sheets',
                                default=True, null=True, blank=True)
    total_votes = models.IntegerField(_("Total number of votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_valid_votes = models.IntegerField(_("Total number of valid votes"), help_text=_("Total number of valid votes"), null=True, blank=True)
    total_invalid_votes = models.IntegerField(_("Total number of invalid votes"), help_text=_("Total number of invalid votes"), null=True, blank=True)
    result_sheet = models.FileField(upload_to=upload_directory_path,
                                    help_text=_("Statement of poll and declaration of results"),
                                    default=None, null=True, blank=True)
    station_agent = models.ForeignKey(
                             "account.User",
                             on_delete=models.CASCADE,
                             help_text=_("Constituency agent that recorded results"),
                             related_name='station_result_sheets',
                             default=None, null=True, blank=True)
    station_approval_at = models.DateTimeField("Date of Stational Approved At", default=None, null=True, blank=True)
    constituency_agent = models.ForeignKey(
                             "account.User",
                             on_delete=models.CASCADE,
                             help_text=_("Constituency agent that recorded results"),
                             related_name='constituency_result_sheets',
                             default=None, null=True, blank=True)
    constituency_approved_at = models.DateTimeField("Constituency Approved At", default=None, null=True, blank=True)
    region_agent = models.ForeignKey(
                             "account.User",
                             on_delete=models.CASCADE,
                             help_text=_("Regional agent that recorded results"),
                             related_name='regional_result_sheets',
                             default=None, null=True, blank=True)
    regional_approval_at = models.DateTimeField("Date of Regional Approved At", default=None, null=True, blank=True)
    nation_agent = models.ForeignKey(
                             "account.User",
                             on_delete=models.CASCADE,
                             help_text=_("National agent that recorded results"),
                             related_name='national_result_sheets',
                             default=None, null=True, blank=True)
    national_approval_at = models.DateTimeField("Date of Regional Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)

    class Meta:
        db_table = 'poll_result_sheet'

    def clean(self):
      self.total_votes = self.total_valid_votes + self.total_invalid_votes


class Result(models.Model):
    '''
    Collates the total number of votes for each party for each office in each constituency. List of fields as follows:
        * office: office being vied for
        * station: the staton the votes were collected from
        * party: the party that votes were collected for
        * votes: total number of votes per constituent
        * file: path to the verification form
        * is_published: has to be vetted and publshed by regional agent before it can be used in results
    '''
    # polling station where the results was collected
    station = models.ForeignKey(
                                "geo.Station",
                                on_delete=models.CASCADE,
                                help_text=_("Polling Station"),
                                related_name='results')
    # candidate voted for
    candidate = models.ForeignKey(
                                 "people.Candidate",
                                 on_delete=models.CASCADE,
                                 help_text=_("Candidate"),
                                 default=None, null=True, blank=True,
                                 related_name='results')
    # total number of votes at station
    votes = models.IntegerField(_("Total number of votes"), help_text=_("Total number of votes"))
    # verification sheet
    result_sheet = models.ForeignKey(
                                    "ResultSheet",
                                    on_delete=models.CASCADE,
                                    help_text=_("Result verification sheet"),
                                    related_name='results',
                                    default=None,  null=True, blank=True)
    # party agent responsible
    station_agent = models.ForeignKey(
                             "account.User",
                             on_delete=models.CASCADE,
                             help_text=_("Station agent that recorded the result"),
                             related_name='results',
                             default=None, null=True, blank=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)

    class Meta:
        db_table = 'poll_result'

    def candidate_details(self):
        if self.candidate is not None:
            if self.candidate.party is not None:
                return f'{self.candidate.full_name} ({self.candidate.party.code})'
        return 'NA'

    '''
    # limit data entry only to constituency agents
    def save(self, *args, **kwargs):
        if not Nation.objects.filter(pk=self.pk).exists() and Nation.objects.exists():
            raise ValidationError('There can be only one instance of this model')
        return super(Nation, self).save(*args, **kwargs)
    '''


class ResultApproval(models.Model):
    result = models.ForeignKey("Result", on_delete=models.CASCADE, help_text=_("Position"))
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    approved_at = models.DateTimeField("Approved At", auto_now_add=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    approving_agent = models.ForeignKey(
                                        "account.User",
                                        on_delete=models.CASCADE,
                                        help_text=_("Agent that approved the result"),
                                        related_name='result_approvals')

    class Meta:
        db_table = 'poll_result_approval'

    def __str__(self):
        return "{} {} {}".format(self.result.position, self.result.station, self.result.votes)

    '''
    # limit data entry only to agents with higher levels than constituency
    # also limit to one approval per level
    def save(self, *args, **kwargs):
        if not Nation.objects.filter(pk=self.pk).exists() and Nation.objects.exists():
            raise ValidationError('There can be only one instance of this model')
        return super(Nation, self).save(*args, **kwargs)
    '''
