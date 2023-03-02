from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from poll.constants import GeoLevelChoices, OfficeChoices
from geo.models import Nation, Region, Constituency, Station
from poll.models.office import Office
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Position(models.Model):

    zone_options = models.Q(app_label='geo', model='Nation') | \
            models.Q(app_label='geo', model='Constituency') | \
            models.Q(app_label='geo', model='Region')

    # name of the positon (cannot be changed after inital migration)
    title = models.CharField("Position name", max_length=255)
    details = models.TextField(blank=True, null=True)
    # actual zone the position contested over
    # optional foreign key for the geo zone being contested
    zone_ct = models.ForeignKey(ContentType,
                                         limit_choices_to=zone_options,
                                         on_delete=models.SET_NULL,
                                         related_name='zones',
                                         null=True, blank=True)
    zone_id = models.PositiveIntegerField(null=True, db_index=True)
    zone = GenericForeignKey('zone_ct', 'zone_id')

    class Meta:
        db_table = 'poll_position'
        # unique_together = ('office', 'zone',)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        # get the actual positon title
        # e.g. Minister for the Volta Region
        return "{} {}".format(self.title, self.zone.title)

    '''
    def clean(self):
        zone = None
        if self.office_id == OfficeChoices.PRESIDENT:
            try:
                presidential_office = Office.objects.filter(level=GeoLevelChoices.NATIONAL).first()
                if presidential_office.exits():
                    try:
                        zone = Nation.objects.filter(pk=self.zone.id).first()
                    except Nation.DoesNotExist:
                        raise ValidationError("Selected position's zone (nation) does not exist. Please select a valid zone (nation)")
            except Office.DoesNotExist:
                raise ValidationError("Selected position's office does not exist. Please select a valid office")
        else:
            try:
                parliamentary_office = Office.objects.filter(level=GeoLevelChoices.CONSTITUENCY).first()
                if parliamentary_office.exits():
                    try:
                        zone = Constituency.objects.filter(pk=self.zone.id).first()
                    except Constituency.DoesNotExist:
                        raise ValidationError("Selected position's zone (constituency) does not exist. Please select a valid zone (constituency)")
            except Office.DoesNotExist:
                raise ValidationError("Selected position's office does not exist. Please select a valid office")
        if zone is None:
            raise ValidationError("Selected position's zone is not valid.")

    @property
    def office_title(self):
        try:
            office = self.office
            return office.title
        except Office.DoesNotExist:
            office = None
        return ''

    @property
    def zone(self):
        try:
            office = self.office
        except Office.DoesNotExist:
            office = None
        if office is None:
            return None
        if office.level == GeoLevelChoices.NATIONAL:
            try:
                return Nation.objects.get(id=self.zone.id)
            except Region.DoesNotExist:
                raise ValidationError("Selected nation does not exist")
        elif office.level == GeoLevelChoices.REGION:
            try:
                return Region.objects.get(id=self.zone.id)
            except Region.DoesNotExist:
                raise ValidationError("Selected region does not exist")
        elif office.level == GeoLevelChoices.CONSTITUENCY:
            try:
                return Constituency.objects.get(id=self.zone.id)
            except Region.DoesNotExist:
                raise ValidationError("Selected constituency does not exist")
        elif office.level == GeoLevelChoices.STATION:
            try:
                return Station.objects.get(id=self.zone.id)
            except Region.DoesNotExist:
                raise ValidationError("Selected station does not exist")
        else:
            raise ValidationError("Invalid office value")
    '''
