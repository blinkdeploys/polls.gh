import os, json
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from poll.models import (
    Event, Office, Position, ResultSheet, Result, ResultApproval,
    SupernationalCollationSheet, NationalCollationSheet, RegionalCollationSheet,
    ConstituencyCollationSheet, StationCollationSheet
)
from people.models import (Agent, Party, Candidate)
from geo.models import (Nation, Region, Constituency, Station)
from poll.constants import StatusChoices, GeoLevelChoices, NameTitleChoices, TerminalColors
from django.contrib.contenttypes.models import ContentType
from poll.utils import intify


class Command(BaseCommand):
    '''Collate results for all the levels and positions'''
    help = 'Collate results for all the levels and positions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='clear all exisitng collations',
        )
        parser.add_argument(
            '--quiet',
            action='store_true',
            help='reduced reporting',
        )
        # parser.add_argument('-models', '--models', type=str, nargs='+', help='The model to run if empty, then all models will be populated')
        # parser.add_argument('-verbose', '--verbose', type=int, nargs='+', help='Run the population showing each line from the scripts')

    def handle(self, *args, **kwargs):

        is_verbose = True
        if kwargs['quiet']:
            is_verbose = False
            
        # clear collations
        if kwargs['clear']:
            supernation_collations = SupernationalCollationSheet.objects.all()
            nation_collations = NationalCollationSheet.objects.all()
            region_collations = RegionalCollationSheet.objects.all()
            constituency_collations = ConstituencyCollationSheet.objects.all()
            station_collations = StationCollationSheet.objects.all()
            total_records = nation_collations.count() \
                            + region_collations.count() \
                            + constituency_collations.count() \
                            + station_collations.count() \
                            + supernation_collations.count()
            # clear_all = input(f'You are about to clear {total_records} collation records, do you want to proceed? Y/N: ')
            # clear_all = f'{clear_all.lower()}'
            # if clear_all in ['y', 'yes']:
            supernation_collations.delete()
            nation_collations.delete()
            region_collations.delete()
            constituency_collations.delete()
            station_collations.delete()
            self.stdout.write(self.style.SUCCESS(f'{total_records} collation results removed from database'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        total = 0

        # transfer data from results to collation
        collated = 0
        sheets = ResultSheet.objects.all()
        for sheet in sheets:
            sub_sheets = sheet.results.all()
            zone_ct = sheet.position.zone_ct
            for sub_sheet in sub_sheets:
                cs, _ = StationCollationSheet.objects \
                            .update_or_create(
                                candidate=sub_sheet.candidate,
                                station=sheet.station,
                                zone_ct=zone_ct,
                                defaults=dict(
                                    total_votes=sub_sheet.votes,
                                )
                            )
                collated += 1
        total += collated
        self.stdout.write(self.style.SUCCESS(f'Station collation completed. {collated} records transfered!'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        # percollate data up from station to constituency
        collated = 0
        sheets = StationCollationSheet.objects.all()
        for sheet in sheets:
            parent_sheet = sheet.station
            zone_ct = sheet.zone_ct
            try:
                cs = ConstituencyCollationSheet.objects \
                                                .filter(
                                                    party=sheet.candidate.party,
                                                    station=parent_sheet,
                                                    zone_ct=zone_ct,
                                                ).first()
                total_votes = intify(cs.total_votes) + intify(sheet.total_votes)
                cs.total_votes = total_votes
                mode = 'U'
            except Exception as e:
                # print(e)
                cs = ConstituencyCollationSheet(
                            party=sheet.candidate.party,
                            station=parent_sheet,
                            zone_ct=zone_ct,
                            total_votes=sheet.total_votes
                        )
                mode = 'C'
            if is_verbose:
                print(f'{TerminalColors.OKBLUE}{mode}{TerminalColors.ENDC} Collating {sheet.total_votes} votes for {sheet.candidate} at the {parent_sheet} station')
            cs.save()
            collated += 1
        total += collated
        self.stdout.write(self.style.SUCCESS(f'Constituency collation completed. {collated} records transfered!'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        # percollate data up from constituency to region
        collated = 0
        sheets = ConstituencyCollationSheet.objects.all()
        for sheet in sheets:
            parent_sheet = sheet.station.constituency
            zone_ct = sheet.zone_ct
            try:
                cs = RegionalCollationSheet.objects \
                                                .filter(
                                                    party=sheet.party,
                                                    constituency=parent_sheet,
                                                    zone_ct=zone_ct,
                                                ).first()
                total_votes = intify(cs.total_votes) + intify(sheet.total_votes)
                cs.total_votes = total_votes
                mode = 'U'
            except Exception as e:
                # print(e)
                cs = RegionalCollationSheet(
                            party=sheet.party,
                            constituency=parent_sheet,
                            zone_ct=zone_ct,
                            total_votes=sheet.total_votes
                        )
                mode = 'C'
            if is_verbose:
                print(f'{TerminalColors.OKBLUE}{mode}{TerminalColors.ENDC} Collating {sheet.total_votes} votes for the {sheet.party.code} in the {parent_sheet} constituency')
            cs.save()
            collated += 1
        total += collated
        self.stdout.write(self.style.SUCCESS(f'Regional collation completed. {collated} records transfered!'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        # percollate data up from region to nation
        collated = 0
        sheets = RegionalCollationSheet.objects.all()
        for sheet in sheets:
            parent_sheet = sheet.constituency.region
            zone_ct = sheet.zone_ct
            try:
                cs = NationalCollationSheet.objects \
                                                .filter(
                                                    party=sheet.party,
                                                    region=parent_sheet,
                                                    zone_ct=zone_ct,
                                                ).first()
                total_votes = intify(cs.total_votes) + intify(sheet.total_votes)
                cs.total_votes = total_votes
                mode = 'U'
            except Exception as e:
                # print(e)
                cs = NationalCollationSheet(
                            party=sheet.party,
                            region=parent_sheet,
                            zone_ct=zone_ct,
                            total_votes=sheet.total_votes
                        )
                mode = 'C'
            if is_verbose:
                print(f'{TerminalColors.OKBLUE}{mode}{TerminalColors.ENDC} Collating {sheet.total_votes} votes for the {sheet.party.code} in the {parent_sheet} region')
            cs.save()
            collated += 1
        total += collated
        self.stdout.write(self.style.SUCCESS(f'National collation completed. {collated} records transfered!'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        # percollate data up from national to supernational
        collated = 0
        sheets = NationalCollationSheet.objects.all()
        for sheet in sheets:
            parent_sheet = sheet.region.nation
            zone_ct = sheet.zone_ct
            try:
                cs = SupernationalCollationSheet.objects \
                                                .filter(
                                                    party=sheet.party,
                                                    nation=parent_sheet,
                                                    zone_ct=zone_ct,
                                                ).first()
                total_votes = intify(cs.total_votes) + intify(sheet.total_votes)
                cs.total_votes = total_votes
                mode = 'U'
            except Exception as e:
                # print(e)
                cs = SupernationalCollationSheet(
                            party=sheet.party,
                            nation=parent_sheet,
                            zone_ct=zone_ct,
                            total_votes=sheet.total_votes
                        )
                mode = 'C'
            if is_verbose:
                print(f'{TerminalColors.OKBLUE}{mode}{TerminalColors.ENDC} Collating {sheet.total_votes} votes for the {sheet.party.code} in the {parent_sheet} nation')
            cs.save()
            collated += 1
        total += collated
        self.stdout.write(self.style.SUCCESS(f'Supernational collation completed. {collated} records transfered!'))
        print(':::::::::::::::::::::::::::::::::::::::::::')

        self.stdout.write(self.style.SUCCESS(f'Collation completed! {total} total records collated.'))
