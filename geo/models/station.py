from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices
# from people.models import Agent
# from django.contrib.contenttypes.models import ContentType


class Station(models.Model):
	code = models.CharField("Constituency code", max_length=25, null=True)
	title = models.CharField("Constituency name", max_length=255)
	details = models.TextField(blank=True, null=True)
	constituency = models.ForeignKey(
		"Constituency", on_delete=models.CASCADE,
		help_text=_("Constituency"),
        related_name='stations')
	status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
	created_at = models.DateTimeField("Created At", auto_now_add=True)

	class Meta:
		db_table = 'geo_station'

	def __str__(self):
		return "{} {}".format(self.code, self.title)

	@property
	def agent(self):
		return self.agent_ct
		# zone_ct = ContentType.objects.get_for_model(Station)
		# return Agent.objects.filter(
		# 				zone_ct=zone_ct,
		# 				zone_id=self.pk
		# 			).first()
