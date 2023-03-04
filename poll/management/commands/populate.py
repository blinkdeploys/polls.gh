import os, json
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from poll.models import (Event, Office, Position, Result, ResultApproval)
from people.models import (Agent, Party, Candidate)
from geo.models import (Nation, Region, Constituency, Station)
from faker import Faker
import random
from poll.constants import StatusChoices, GeoLevelChoices, NameTitleChoices
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

        # print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(constituency)
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

    if name == "position":
        # remove all positions
        Position.objects.all().delete()
        NATIONAL_COUNT = 1
        # create all national positions
        count = 0
        nation = Nation.objects.first()
        office = Office.objects.filter(level=GeoLevelChoices.NATIONAL).first()
        zone_ct = ContentType.objects.get_for_model(Nation)
        for i in range(0, NATIONAL_COUNT):
            zone = nation
            # title = f'The President {nation.title}' if i == 1 else f'Vice-President {nation.title}'
            title = f'The President {nation.title}'
            model = Position(
                    title=title,
                    details=faker.sentence(),
                    zone_ct=zone_ct,
                    zone_id=zone.pk)
            # model.full_clean()
            model.save()
            count = count + 1
        print(f'{count} National positions created successfully')

        # create all constituency positions
        count = 0
        zone_ct = ContentType.objects.get_for_model(Constituency)
        constituencies = Constituency.objects.all()
        for constituency in constituencies:
            zone = constituency
            title = f'Parliamentary Representative, {constituency.title} Consotituency'
            model = Position(
                    title=title,
                    details=faker.sentence(),
                    zone_ct=zone_ct,
                    zone_id=zone.pk)
            # model.full_clean()
            model.save()
            count = count + 1
        print(f'{count} Constituency positions created successfully')
        print(f'Data imported successfully')
        return (True, None)

    if name == "result":
        MAX_VOTES = 14
        MAX_STATION = 5
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
                    total_votes = 0
                    if random.randint(0, VOTE_OR_NOT_MAX) == 1:
                        total_votes = random.randint(0, MAX_VOTES)
                        result = Result(
                            candidate=candidate,
                            station=station,
                            total_votes=total_votes,
                            constituency_agent_id=None,
                            result_sheet=None)
                        result.full_clean()
                        result.save()
                        count = count + 1
                total_count = total_count + count
            print(f'{count} Polling stations recorded for candidate {candidate.full_name}')
        print(f'{total_count} Results created successfully')
        return (True, None)

    '''
    if name == "result_approval":
        model = ResultApproval
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                        title=row['title']))


    # people

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

    if name == "agent":
        model = Agent
        if model.objects.count() <= 80:
            return (exists, model(
                        first_name=faker.first_name(),
                        last_name=faker.last_name(),
                        email=faker.email(),
                        phone=faker.phone(),
                        address=faker.sentence(),
                        description=faker.sentence(),
                        status_id=1))
    '''

    if name == "candidate":
        model = Candidate
        # ensure that there are at least one candidate for each position for each party
        parties = Party.objects.all()
        positions = Position.objects.all()
        print("Deleting all candidate records (y/n)?")
        Candidate.objects.all().delete()
        total = 0
        for party in parties:
            count = 0
            for position in positions:
                if random.randint(0, 10) == 1:
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
            print(f'{count} {party.title} Candidates created successfully.')
        print(f'{total} Candidates created successfully.')
        return (False, None)

    if name == "party":
        model = Party
        exists = model.objects.filter(id=row['id']).first()
        return (exists, model(id=row['id'],
                        code=row['code'],
                        title=row['title']))


    return False, None


class Command(BaseCommand):
    '''
    Import data from a JSON file into a Listings table
    python manage.py import_json_data.
    '''
    help = 'Import data from a JSON file into a Listings table'

    def add_arguments(self, parser):
        # parser.add_argument('file_path', type=str, help='The path to the JSON file')
        pass

    def handle(self, *args, **kwargs):
        # file_path = kwargs['file_path']

        json_files = get_all_files()
        found_tables = []
        seeded = []
        for json_file in sorted(json_files):
            print(json_file)
            try:
                with open(f"{JSON_PATH}{json_file}") as json_file_content:
                    data = json.load(json_file_content)
                    imported = 0
                    found = 0

                    exists, model = get_model(data["name"], data["data"][0])

                    if model is not None:
                        i = 0
                        for row in data["data"]:
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
                                        self.stdout.write(self.style.SUCCESS(f'Data imported successfully'))
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

