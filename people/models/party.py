from django.db import models
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices

class Party(models.Model):
	code = models.CharField("Party accronym", max_length=10)
	title = models.CharField("Party name", max_length=255)
	details = models.TextField(blank=True, null=True)
	agent = models.ForeignKey(
							  "people.Agent", on_delete=models.CASCADE,
							  help_text=_("Agent in command"),
							  null=True, blank=True,
							  related_name='parties')
	status = models.CharField(max_length=35, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
	created_at = models.DateTimeField("Created At", auto_now_add=True)
	
	class Meta:
		db_table = 'poll_party'

	def __str__(self):
		return self.title

	@property
	def result_votes(self):
		votes = 0
		candidates = self.candidates.all()
		for candidate in candidates:
			for result in candidate.results.all():
				votes = votes + int(result.votes)
		return votes

	def total_candidates(self):
		return self.candidates.all().count()
