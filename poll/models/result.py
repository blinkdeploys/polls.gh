from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import GeoLevelChoices, StatusChoices
from poll.utils import upload_directory_path
from django.core.exceptions import ValidationError
from poll.utils import intify
from django.contrib.contenttypes.models import ContentType


ZONE_OPTIONS = models.Q(app_label='geo', model='Nation') | \
        models.Q(app_label='geo', model='Constituency')
        # models.Q(app_label='geo', model='Region') | \
        # models.Q(app_label='geo', model='Station') | \
# zone_id = models.PositiveIntegerField(null=True, db_index=True)
# zone = GenericForeignKey('zone_ct', 'zone_id')


# class PresidentialSummarySheet(models.Model):
#     pass


class ParliamentarySummarySheet(models.Model):
    position = models.OneToOneField("poll.Position",
                                on_delete=models.CASCADE,
                                help_text=_("Position"),
                                related_name='parliamentary_summary_sheet',
                                default=True, null=True, blank=True)
    candidate = models.OneToOneField("people.Candidate",
                                  on_delete=models.CASCADE,
                                  help_text=_("Candidate"),
                                  default=None, null=True, blank=True,
                                  related_name='parliamentary_summary_sheet')
    constituency = models.OneToOneField("geo.Constituency",
                                on_delete=models.CASCADE,
                                help_text=_("Constituency"),
                                default=None, null=True, blank=True,
                                related_name='parliamentary_summary_sheet')
    votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    # TODO: To capture Variance with EC Summary

    class Meta:
        db_table = 'poll_parliamentary_summary_sheet'

    def clean(self):
        self.votes = intify(self.votes)
        self.total_votes = intify(self.total_votes)


class SupernationalCollationSheet(models.Model):
    party = models.ForeignKey("people.Party",
                                on_delete=models.CASCADE,
                                help_text=_("Party"),
                                related_name='supernational_collation_sheets',
                                default=None, null=True, blank=True)
    nation = models.ForeignKey("geo.Nation",
                                on_delete=models.CASCADE,
                                help_text=_("Nation"),
                                related_name='supernational_collation_sheets',
                                default=None, null=True, blank=True)
    total_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes_ec = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)
    zone_ct = models.ForeignKey(ContentType,
                                limit_choices_to=ZONE_OPTIONS,
                                on_delete=models.SET_NULL,
                                related_name='supernational_collation_zones',
                                default=None, null=True, blank=True)

    class Meta:
        db_table = 'poll_supernational_collation_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


class NationalCollationSheet(models.Model):
    party = models.ForeignKey("people.Party",
                                on_delete=models.CASCADE,
                                help_text=_("Party"),
                                default=None, null=True, blank=True,
                                related_name='national_collation_sheets')
    region = models.ForeignKey("geo.Region",
                                on_delete=models.CASCADE,
                                help_text=_("Region"),
                                default=None, null=True, blank=True,
                                related_name='national_collation_sheets')
    total_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes_ec = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    nation_agent = models.ForeignKey("people.Agent",
                             on_delete=models.CASCADE,
                             help_text=_("National agent that recorded results"),
                             related_name='national_collation_sheets',
                             default=None, null=True, blank=True)
    national_approval_at = models.DateTimeField("Date of Regional Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)
    zone_ct = models.ForeignKey(ContentType,
                                limit_choices_to=ZONE_OPTIONS,
                                on_delete=models.SET_NULL,
                                related_name='national_collation_zones',
                                default=None, null=True, blank=True)

    class Meta:
        db_table = 'poll_national_collation_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


class RegionalCollationSheet(models.Model):
    party = models.ForeignKey("people.Party",
                                  on_delete=models.CASCADE,
                                  help_text=_("Party"),
                                  default=None, null=True, blank=True,
                                  related_name='regional_collation_sheets')
    constituency = models.ForeignKey("geo.Constituency",
                                on_delete=models.CASCADE,
                                help_text=_("Constituency"),
                                default=None, null=True, blank=True,
                                related_name='regional_collation_sheets')
    total_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes_ec = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    region_agent = models.ForeignKey("people.Agent",
                             on_delete=models.CASCADE,
                             help_text=_("Regional agent that recorded results"),
                             related_name='regional_collation_sheets',
                             default=None, null=True, blank=True)
    regional_approval_at = models.DateTimeField("Date of Regional Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)
    zone_ct = models.ForeignKey(ContentType,
                                limit_choices_to=ZONE_OPTIONS,
                                on_delete=models.SET_NULL,
                                related_name='regional_collation_zones',
                                default=None, null=True, blank=True)

    class Meta:
        db_table = 'poll_regional_collation_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


class ConstituencyCollationSheet(models.Model):
    party = models.ForeignKey("people.Party",
                                  on_delete=models.CASCADE,
                                  help_text=_("Party"),
                                  default=None, null=True, blank=True,
                                  related_name='constituency_collation_sheets')
    station = models.ForeignKey("geo.Station",
                                on_delete=models.CASCADE,
                                help_text=_("Station"),
                                default=None, null=True, blank=True,
                                related_name='constituency_collation_sheets')
    total_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes_ec = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    constituency_agent = models.ForeignKey("people.Agent",
                             on_delete=models.CASCADE,
                             help_text=_("Constituency agent that recorded results"),
                             related_name='constituency_collation_sheets',
                             default=None, null=True, blank=True)
    constituency_approved_at = models.DateTimeField("Constituency Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)
    zone_ct = models.ForeignKey(ContentType,
                                limit_choices_to=ZONE_OPTIONS,
                                on_delete=models.SET_NULL,
                                related_name='constituency_collation_zones',
                                default=None, null=True, blank=True)

    class Meta:
        db_table = 'poll_constituency_collation_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


class StationCollationSheet(models.Model):
    candidate = models.ForeignKey("people.Candidate",
                                  on_delete=models.CASCADE,
                                  help_text=_("Candidate"),
                                  default=None, null=True, blank=True,
                                  related_name='station_collation_sheets')
    station = models.ForeignKey("geo.Station",
                                on_delete=models.CASCADE,
                                help_text=_("Polling Station"),
                                default=None, null=True, blank=True,
                                related_name='station_collation_sheets')
    total_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of votes"), null=True, blank=True)
    total_votes_ec = models.IntegerField(_("EC Summary Collation totals"), help_text=_("EC Collation number"), null=True, blank=True)
    station_agent = models.ForeignKey("people.Agent",
                             on_delete=models.CASCADE,
                             help_text=_("Constituency agent that recorded results"),
                             related_name='station_collation_sheets',
                             default=None, null=True, blank=True)
    station_approval_at = models.DateTimeField("Date of Stational Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)
    zone_ct = models.ForeignKey(ContentType,
                                limit_choices_to=ZONE_OPTIONS,
                                on_delete=models.SET_NULL,
                                related_name='station_collation_zones',
                                default=None, null=True, blank=True)

    class Meta:
        db_table = 'poll_station_collation_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


class ResultSheet(models.Model):
    station = models.ForeignKey("geo.Station",
                                on_delete=models.CASCADE,
                                help_text=_("Polling Station"),
                                related_name='result_sheets',
                                default=True, null=True, blank=True)
    position = models.ForeignKey("poll.Position",
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
    station_agent = models.ForeignKey("people.Agent",
                             on_delete=models.CASCADE,
                             help_text=_("Constituency agent that recorded results"),
                             related_name='result_sheets',
                             default=None, null=True, blank=True)
    station_approval_at = models.DateTimeField("Date of Stational Approved At", default=None, null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, blank=True, null=True)

    class Meta:
        db_table = 'poll_result_sheet'

    def clean(self):
        self.total_votes = intify(self.total_votes)


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
                             "people.Agent",
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

    def clean(self):
        self.votes = intify(self.votes)

    def save(self, *args, **kwargs):
        total_votes=0
        total_votes_ec=0
        try:
            collation_sheet = StationCollationSheet.objects \
                                        .filter(
                                            candidate=self.candidate,
                                            station=self.station,
                                        ).first()
            collation_sheet.total_votes = collation_sheet.total_votes + self.total_votes
            collation_sheet.total_votes_ec = collation_sheet.total_votes_ec + self.total_votes_ec
        except Exception as e:
            collation_sheet = StationCollationSheet(
                                            candidate=self.candidate,
                                            station=self.station,
                                            total_votes=total_votes,
                                            total_votes_ec=total_votes_ec,
                                        )
        collation_sheet.save()
        super().save(*args, **kwargs)


class ResultApproval(models.Model):
    result = models.ForeignKey("Result", on_delete=models.CASCADE, help_text=_("Position"))
    status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    approved_at = models.DateTimeField("Approved At", auto_now_add=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    approving_agent = models.ForeignKey(
                                        "people.Agent",
                                        on_delete=models.CASCADE,
                                        help_text=_("Agent that approved the result"),
                                        related_name='result_approvals')

    class Meta:
        db_table = 'poll_result_approval'

    def __str__(self):
        return "{} {} {}".format(self.result.position, self.result.station, self.result.votes)



'''
total_valid_votes = models.IntegerField(_("Collation total number of valid votes"), help_text=_("Total number of valid votes"), null=True, blank=True)
total_invalid_votes = models.IntegerField(_("Collation total number of invalid votes"), help_text=_("Total number of invalid votes"), null=True, blank=True)
'''


'''
    def save(self, *args, **kwargs):
        collation_sheets = []
        try:
            collation_sheets = StationCollationSheet.objects \
                                .filter(
                                    candidate=self.candidate,
                                    station__in=self.constituency.stations,
                                ).all()
        except Exception as e:
            print(e)

        total_votes = 0
        total_invalid_votes = 0
        total_valid_votes = 0
        for collation_sheet in collation_sheets:
            total_votes += collation_sheet.total_votes if type(collation_sheet.total_votes) is int else 0
            total_invalid_votes += collation_sheet.total_invalid_votes if type(collation_sheet.total_invalid_votes) is int else 0
            total_valid_votes += collation_sheet.total_valid_votes if type(collation_sheet.total_valid_votes) is int else 0
        self.total_votes = total_votes
        self.total_invalid_votes = total_invalid_votes
        self.total_valid_votes = total_valid_votes
        super().save(*args, **kwargs)
'''

'''
    def save(self, *args, **kwargs):
        total_votes=0,
        total_valid_votes=0,
        total_invalid_votes=0,
        try:
            collation_sheet = NationalCollationSheet.objects \
                                        .filter(
                                            candidate=self.candidate,
                                            region=self.constituency.region,
                                        ).first()
        except Exception as e:
            collation_sheet = NationalCollationSheet.objects \
                                        .create(
                                            candidate=self.candidate,
                                            region=self.constituency.region,
                                            total_votes=total_votes,
                                            total_valid_votes=total_valid_votes,
                                            total_invalid_votes=total_invalid_votes,
                                        )
        collation_sheet.total_valid_votes = collation_sheet.total_valid_votes + self.total_valid_votes
        collation_sheet.total_invalid_votes = collation_sheet.total_invalid_votes + self.total_invalid_votes
        collation_sheet.total_votes = collation_sheet.total_valid_votes + collation_sheet.total_invalid_votes
        collation_sheet.save()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        total_votes=0,
        total_valid_votes=0,
        total_invalid_votes=0,
        try:
            collation_sheet = NationalCollationSheet.objects \
                                        .filter(
                                            candidate=self.candidate,
                                            region=self.constituency.region,
                                        ).first()
        except Exception as e:
            collation_sheet = NationalCollationSheet.objects \
                                        .create(
                                            candidate=self.candidate,
                                            region=self.constituency.region,
                                            total_votes=total_votes,
                                            total_valid_votes=total_valid_votes,
                                            total_invalid_votes=total_invalid_votes,
                                        )
        collation_sheet.total_valid_votes = collation_sheet.total_valid_votes + self.total_valid_votes
        collation_sheet.total_invalid_votes = collation_sheet.total_invalid_votes + self.total_invalid_votes
        collation_sheet.total_votes = collation_sheet.total_valid_votes + collation_sheet.total_invalid_votes
        collation_sheet.save()
        super().save(*args, **kwargs)


    def clean(self):
      self.total_valid_votes = self.total_valid_votes if type(self.total_valid_votes) is int else 0
      self.total_invalid_votes = self.total_invalid_votes if type(self.total_invalid_votes) is int else 0
      if self.total_votes != self.total_valid_votes + self.total_invalid_votes:
          self.total_votes = self.total_valid_votes + self.total_invalid_votes


'''

'''
        # Ensure that every result has a parent result sheet and collate votes up

        # exists = False
        # result_sheet = None
        # position = None

        # if self.result_sheet is not None:
        #     result_sheet = ResultSheet.objects.filter(pk=self.result_sheet.pk).first()
        #     if result_sheet is not None:
        #         exists = True
        # if exists is False:
        #     raise ValidationError(f'Valid result sheet not found for result {self.pk}')

        # if result_sheet.position is not None:
        #     position = Position.objects.filter(pk=result_sheet.position.pk).exists()
        #     if position is not None:
        #         exists = True
        # if exists is False:
        #     raise ValidationError(f'Valid position is not found for result sheet {result_sheet.pk}.')

        # sum up the total valid votes
        total_valid_votes = 0
        winning_candidates = None
        max_votes = 0
        result_scores = dict()
        for result in self.results.all():
            result_votes = result.votes if type(result.votes) is int and result.votes > 0 else 0
            total_valid_votes += result_votes
            result_score = result_scores.get(result_votes, [])
            result_score[result_votes].append(result.candidate)
            if max_votes < result_votes:
                max_votes = result_votes

        # total votes
        result.total_valid_votes = total_valid_votes
        self.total_votes = self.total_invalid_votes + self.total_valid_votes

        # winning candidate
        winning_candidates = result_scores.get(max_votes, [])
        self.winning_candidate = winning_candidates

        return super(ResultSheet, self).save(*args, **kwargs)
''''''
    # constituency_collation_sheet = models.ForeignKey(
    #                          "people.ConstituencyCollationSheet",
    #                          on_delete=models.CASCADE,
    #                          help_text=_("Collation sheet for the result sheet"),
    #                          related_name='result_sheets',
    #                          default=None, null=True, blank=True)
'''
'''
# limit data entry only to agents with higher levels than constituency
# also limit to one approval per level
def save(self, *args, **kwargs):
    if not Nation.objects.filter(pk=self.pk).exists() and Nation.objects.exists():
        raise ValidationError('There can be only one instance of this model')
    return super(Nation, self).save(*args, **kwargs)
'''
