from django.db import models

ROWS_PER_PAGE = 20

class NameTitleChoices(models.TextChoices):
    MR='Mr.'
    MRS='Mrs.'
    MISS='Miss'
    SR='Sr.'
    ESQR='Esqr.'

class StatusChoices(models.TextChoices):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class RoleChoices(models.TextChoices):
    UNASSIGNED = "Unassigned"
    AGENT = "Agent"
    CANDIDATE = "Candidate"
    MONITORING = "Monitoring"

class GeoLevelChoices(models.IntegerChoices):
    UNASSIGNED = 0
    STATION = 1
    CONSTITUENCY = 2
    REGION = 3
    NATIONAL = 4

class OfficeChoices(models.TextChoices):
    PRESIDENT=(1, "President")
    PARLIAMENT=(2, "Parliament")

