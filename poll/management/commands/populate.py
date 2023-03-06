import os, json
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from poll.models import (Event, Office, Position, ResultSheet, Result, ResultApproval)
from people.models import (Agent, Party, Candidate)
from geo.models import (Nation, Region, Constituency, Station)
from faker import Faker
import random
from poll.constants import StatusChoices, GeoLevelChoices, NameTitleChoices, TerminalColors
from django.contrib.contenttypes.models import ContentType


faker = Faker()

JSON_PATH = 'sql/poll/'
STATUS_COUNT = len(StatusChoices.choices)

def get_all_files():
    return [pos_json for pos_json in os.listdir(JSON_PATH) if pos_json.endswith('.json')]

def get_model(name, row, count=0):

    # geo

    if name == "nation":
        model = Nation
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                            code=row['code'],
                            title=row['title']))

    if name == "region":
        model = Region
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                      title=row['title'],
                      nation_id=1))

    if name == "constituency":
        model = Constituency
        count = count + 1
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                              region_id=row['region_id'],
                              title=row['title']))

    if name == "station":
        model = Station
        exists = model.objects.filter(
            title=row['title']
        ).first()

        constituency = row.get('constituency_id', None)

        if constituency is None:
            return False, None
        else:
            if type(constituency) is str:
                constituency = Constituency.objects.filter(title=constituency).first()
                if constituency is not None:
                    constituency = constituency.pk

        # print(count, row['id'], constituency, type(constituency))
        record = model(
                        code=row['code'],
                        constituency_id=int(constituency),
                        title=row['title'])
        return (exists, record)

    # poll
    '''

    if name == "event":
        model = Event
        Event.objects.all().delete()
        offices = Office.objects.all()
        for office in offices:
            yr = faker.year()
            mth = faker.month()
            day = faker.day()
            start = f'{day}-{mth}-{yr}'
            end = f'{day + 1}-{mth}-{yr}'
            title = f'{office.title} Elections {yr}'
            if title is not None:
                model = Event(
                            title=title,
                            details=faker.sentence(),
                            office=office,
                            start=start,
                            end=end,
                            status_id=1)
                count = count + 1
        print(f'{count} Election events successfully created')
        return False, None

    if name == "office":
        model = Office
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                        level=row['level'],
                        title=row['title']))
    '''

    if name == "position":
        positions_to_create = []
        nfound = 0
        cfound = 0

        # find national positions that have not been created
        ncount = 0
        zone_ct = ContentType.objects.get_for_model(Nation)
        positions = Position.objects.filter(zone_ct__in=[zone_ct]).all()
        position_ids = [p.zone_id for p in positions]
        nfound = len(position_ids)
        locations = Nation.objects.all()
        if positions.count() < locations.count():
            zones = Nation.objects.exclude(pk__in=position_ids).all()
            for zone in zones:
                positions_to_create = positions_to_create + [Position(
                    title=f'The President, {zone.title}',
                    zone_ct=zone_ct,
                    zone_id=zone.pk,
                    details=faker.sentence(),
                )]
                ncount = ncount + 1

        # find parliamentary positions that have not been created
        ccount = 0
        zone_ct = ContentType.objects.get_for_model(Constituency)
        positions = Position.objects.filter(zone_ct__in=[zone_ct]).all()
        position_ids = [p.zone_id for p in positions]
        cfound = len(position_ids)
        locations = Constituency.objects.all()
        if positions.count() < locations.count():
            zones = Constituency.objects.exclude(pk__in=position_ids).all()
            for zone in zones:
                positions_to_create = positions_to_create + [Position(
                    title=f'Parliamentary Representative, {zone.title} Consotituency',
                    zone_ct=zone_ct,
                    zone_id=zone.pk,
                    details=faker.sentence(),
                )]
                ccount = ccount + 1

        count = 0
        for position_to_create in positions_to_create:
            position_to_create.save()
            count = count + 1

        print(f'{TerminalColors.OKGREEN}{nfound} National positions found, {cfound} Constituency positions found{TerminalColors.ENDC}')
        if count > 0:
            print(f'{TerminalColors.OKGREEN}{count} Positions created successfully ({ncount} National, {ccount} Constituencies){TerminalColors.ENDC}')

        return (True, None)

    '''
    if name == "result":
        MAX_VOTES = 53
        MAX_STATION = 3
        VOTE_OR_NOT_MAX = 3
        model = Result
        # delete all results
        Result.objects.all().delete()
        # create all results
        count = 0
        total_count = 0
        stations = Station.objects.all()
        candidates = Candidate.objects.all()
        for candidate in candidates:
            count = 0
            if random.randint(0, MAX_STATION) == 1:
                for station in stations:
                    print(candidate, station)
                    votes = 0
                    if random.randint(0, VOTE_OR_NOT_MAX) == 1:
                        votes = random.randint(0, MAX_VOTES)
                        result_sheet = ResultSheet.objects \
                                        .filter(
                                            station=station,
                                            position=candidate.position,
                                        ).first()
                        result = Result(
                                        candidate=candidate,
                                        station=station,
                                        votes=votes,
                                        result_sheet=result_sheet,
                                        station_agent_id=None)
                        # print(result.__dict__)
                        result.full_clean()
                        result.save()
                        count = count + 1
                total_count = total_count + count
            print(f'{TerminalColors.OKGREEN}{count} Polling stations recorded for candidate {candidate.full_name}{TerminalColors.ENDC}')
        print(f'{TerminalColors.OKGREEN}{total_count} Results created successfully{TerminalColors.ENDC}')
        return (True, None)
    '''

    # people

    if name == "candidate":
        model = Candidate
        # ensure that there are at least one candidate for each position for each party
        parties = Party.objects.all()
        print("Deleting all candidate records (y/n)?")
        Candidate.objects.all().delete()

        total = 0
        # POSITION_HAS_CANDIDATE_MAX=3

        positions = Position.objects.filter(zone_ct__in=[ContentType.objects.get_for_model(Nation)]).all()
        for party in parties:
            count = 0
            for position in positions:
                print(position, party)
                ismof = random.randint(0, 1)
                prefix = faker.prefix_male()
                first_name = faker.first_name_male()
                if ismof == 0:
                    prefix = faker.prefix_female()
                    first_name = faker.first_name_female()
                model = Candidate(
                            prefix=prefix,
                            first_name=first_name,
                            last_name=faker.last_name(),
                            other_names=faker.first_name(),
                            description=faker.sentence(),
                            party=party,
                            position=position,
                            status=StatusChoices.ACTIVE
                )
                model.full_clean()
                model.save()
                count = count + 1
                total = total + count
            print(f'{TerminalColors.OKGREEN}{count} {party.title} Presidential Candidates created successfully.{TerminalColors.ENDC}')

        positions = Position.objects.filter(zone_ct__in=[ContentType.objects.get_for_model(Constituency)]).all()
        for party in parties:
            count = 0
            for position in positions:
                print(position, party)
                # if random.randint(0, POSITION_HAS_CANDIDATE_MAX) == 1:
                ismof = random.randint(0, 1)
                prefix = faker.prefix_male()
                first_name = faker.first_name_male()
                if ismof == 0:
                    prefix = faker.prefix_female()
                    first_name = faker.first_name_female()
                model = Candidate(
                            prefix=prefix,
                            first_name=first_name,
                            last_name=faker.last_name(),
                            other_names=faker.first_name(),
                            description=faker.sentence(),
                            party=party,
                            position=position,
                            status=StatusChoices.ACTIVE
                )
                model.full_clean()
                model.save()
                count = count + 1
                total = total + count
            print(f'{TerminalColors.OKGREEN}{count} {party.title} Candidates created successfully.{TerminalColors.ENDC}')
        print(f'{TerminalColors.OKGREEN}{total} Parliamentary Candidates created successfully.{TerminalColors.ENDC}')

        return (False, None)

    if name == "party":
        model = Party
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                        code=row['code'],
                        title=row['title']))


    '''
    if name == "result_sheet":
        total = 0
        print('deleting result sheets...')
        ResultSheet.objects.all().delete()
        stations = Station.objects.all()
        positions = Position.objects.filter(zone_ct__in=[ContentType.objects.get_for_model(Nation)]).all()
        for position in positions:
            count = 0
            for station in stations:
                model = ResultSheet(
                        position=position,
                        station=station,
                        total_votes=0,
                        total_valid_votes=0,
                        total_invalid_votes=0,
                        result_sheet=None,
                        station_agent=None,
                        station_approval_at=None,
                        constituency_agent=None,
                        constituency_approved_at=None,
                        region_agent=None,
                        regional_approval_at=None,
                        nation_agent=None,
                        national_approval_at=None,
                        status=StatusChoices.ACTIVE,
                )
                model.full_clean()
                model.save()
                count = count + 1
                total = total + 1
            print(f'{count} {position} Presidential Result Sheets created successfully')
        positions = Position.objects.filter(zone_ct__in=[ContentType.objects.get_for_model(Constituency)]).all()
        for position in positions:
            count = 0
            for station in stations:
                model = ResultSheet(
                        position=position,
                        station=station,
                        total_votes=0,
                        total_valid_votes=0,
                        total_invalid_votes=0,
                        result_sheet=None,
                        station_agent=None,
                        station_approval_at=None,
                        constituency_agent=None,
                        constituency_approved_at=None,
                        region_agent=None,
                        regional_approval_at=None,
                        nation_agent=None,
                        national_approval_at=None,
                        status=StatusChoices.ACTIVE,
                )
                model.full_clean()
                model.save()
                count = count + 1
                total = total + 1
            print(f'{count} {position} Parliamentary Result Sheets created successfully')
        print(f'{total} Data records imported successfully')
        return (True, None)
    '''


    '''
    if name == "result_approval":
        model = ResultApproval
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                        title=row['title']))

    if name == "user":
        model = User
        exists = model.objects.filter(id=row['id']).first()
        model = User(
                password=password,
                email=faker.unique().email(),
                username=faker.username(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                date_join=now(),
                is_active=False,
                is_staff=False,
                is_superuser=False,
            )
        model.set_password(password)
        model.save()
        return True, None
    '''

    if name == "agent":
        model = Agent
    	
        zone_models = [Nation, Region, Constituency, Station]

        for zone_model in zone_models:
            zones = zone_model.objects.all()
            zone_ct = ContentType.objects.get_for_model(zone_model)
            for zone in zones:
                defaults = dict(
                                first_name=faker.first_name(),
                                last_name=faker.last_name(),
                                email=faker.email(),
                                phone=faker.phone_number(),
                                address=faker.sentence(),
                                description=faker.sentence(),
                                status=StatusChoices.ACTIVE
                )
                print(defaults.get('first_name', ''), defaults.get('last_name', ''), defaults.get('email', ''))
                model = Agent.objects.update_or_create(
                        zone_ct=zone_ct,
                        zone_id=zone.pk,
                        defaults=defaults)
        return True, None


    return False, None


class Command(BaseCommand):
    '''
    Import data from a JSON file into a Listings table
    python manage.py import_json_data.
    '''
    help = 'Import data from a JSON file into a Listings table'

    def add_arguments(self, parser):
        parser.add_argument('-models', '--models', type=str, nargs='+', help='The model to run if empty, then all models will be populated')
        parser.add_argument('-verbose', '--verbose', type=int, nargs='+', help='Run the population showing each line from the scripts')

    def handle(self, *args, **kwargs):

        models_to_use = kwargs['models']
        use_single_model = False
        if models_to_use is not None:
            use_single_model = len(models_to_use) > 0
            models_to_use = models_to_use.split(' ')

        use_verbose = kwargs['verbose']
        if use_verbose is not None:
            use_verbose = int(use_verbose) > 1

        json_files = get_all_files()
        found_tables = []
        seeded = []
        for json_file in sorted(json_files):
            print(f'Processing {json_file}...')
            try:
                with open(f"{JSON_PATH}{json_file}") as json_file_content:
                    data = json.load(json_file_content)
                    imported = 0
                    found = 0

                    if use_single_model is False or (use_single_model is True and data["data"][0] in models_to_use):
                        exists, model = get_model(data["name"], data["data"][0])
                        if model is not None:
                            i = 0
                            for row in data["data"]:
                                if use_verbose:
                                    print(row)
                                if data["name"] not in found_tables:
                                    found_tables.append(data["name"])
                                exists, model = get_model(data["name"], row, i)
                                i = i + 1
                                if exists:
                                    found = found + 1
                                else:
                                    try:
                                        if model is not None:
                                            model.full_clean()
                                            model.save()
                                            # self.stdout.write(self.style.SUCCESS(f'Data imported successfully'))
                                            imported = imported + 1
                                            if data["name"] not in seeded:
                                                seeded.append(data["name"])
                                    except ValidationError as e:
                                        self.stderr.write(f'Error: {e}')
                            if found > 0:
                                self.stdout.write(self.style.SUCCESS(f'{found} records found for model {data["name"]}'))
                            if imported > 0:
                                self.stdout.write(self.style.SUCCESS(f'{imported} recordds successfully imported {data["name"]}'))
                            else:
                                self.stdout.write(self.style.ERROR(f'No data imported for {data["name"]}'))

            except FileNotFoundError:
                raise FileNotFoundError(f'Fixture file {json_file} not in folder')
        self.stdout.write(self.style.SUCCESS(f'Done: {len(json_files)} total tables checked, {len(found_tables)} tables found, {len(seeded)} tables seeded'))

