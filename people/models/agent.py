from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from geo.models import Nation, Region, Constituency, Station


class Agent(models.Model):

	zone_options = models.Q(app_label='geo', model='Nation') | \
            models.Q(app_label='geo', model='Region') | \
            models.Q(app_label='geo', model='Constituency') | \
            models.Q(app_label='geo', model='Station')

	first_name = models.CharField("First name", max_length=255)
	last_name = models.CharField("Last name", max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=50)
	address =  models.TextField(blank=True, null=True)
	zone_ct = models.ForeignKey(ContentType,
								limit_choices_to=zone_options,
								on_delete=models.SET_NULL,
								related_name='agent_ct',
								null=True, blank=True)
	zone_id = models.PositiveIntegerField(null=True, db_index=True)
	zone = GenericForeignKey('zone_ct', 'zone_id')
	user = models.OneToOneField(
		"account.User",
		on_delete=models.SET_NULL,
        # primary_key=True,
		related_name="agent",
		default=None, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
	created_at = models.DateTimeField("Created At", auto_now_add=True)

	class Meta:
		db_table = 'people_agent'

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	@property
	def full_name(self):
		return f'{self.first_name} {self.last_name}'

	@property
	def zone_title(self):
		try:
			if self.zone_ct == ContentType.objects.get_for_model(Nation):
				return Nation.objects.get(pk=self.zone_id).title
			elif self.zone_ct == ContentType.objects.get_for_model(Region):
				return Region.objects.get(pk=self.zone_id).title
			elif self.zone_ct == ContentType.objects.get_for_model(Constituency):
				return Constituency.objects.get(pk=self.zone_id).title
			elif self.zone_ct == ContentType.objects.get_for_model(Station):
				return Station.objects.get(pk=self.zone_id).title
		except Exception as e:
			print(e)
		return ''
		
	@property
	def zone_type(self):
		if self.zone_ct == ContentType.objects.get_for_model(Nation):
			return 'National'
		elif self.zone_ct == ContentType.objects.get_for_model(Region):
			return 'Region'
		elif self.zone_ct == ContentType.objects.get_for_model(Constituency):
			return 'Constituency'
		elif self.zone_ct == ContentType.objects.get_for_model(Station):
			return 'Polling Station'
		return 'N/A'
