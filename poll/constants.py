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

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
