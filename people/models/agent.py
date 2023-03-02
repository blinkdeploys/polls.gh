from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices

class Agent(models.Model):
	first_name = models.CharField("First name", max_length=255)
	last_name = models.CharField("Last name", max_length=255)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	address =  models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
	created_at = models.DateTimeField("Created At", auto_now_add=True)
	
	class Meta:
		db_table = 'people_agent'

	def __str__(self):
		return self.first_name