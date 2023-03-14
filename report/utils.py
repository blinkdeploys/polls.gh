from poll.utils import intify
from django.contrib.contenttypes.models import ContentType
from poll.models import (Position, Result, ResultSheet, SupernationalCollationSheet,
                         NationalCollationSheet, RegionalCollationSheet,
                         ConstituencyCollationSheet, StationCollationSheet,
                         ParliamentarySummarySheet)
from people.models import Candidate
from geo.models import Nation, Region, Constituency, Station
from poll.constants import TerminalColors


def clear_collated_results():
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
    return total_records


def collate_results(can_clear=True, is_verbose=False):

    if can_clear:
        total_records = clear_collated_results()
        print(f'{TerminalColors.OKBLUE}{total_records} collation results removed from database{TerminalColors.ENDC}')
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
    print(f'{TerminalColors.OKBLUE}Station collation completed. {collated} records transfered.{TerminalColors.ENDC}')
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
    print(f'{TerminalColors.OKBLUE}Constituency collation completed. {collated} records transfered.{TerminalColors.ENDC}')
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
    print(f'{TerminalColors.OKBLUE}Regional collation completed. {collated} records transfered.{TerminalColors.ENDC}')
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
    print(f'{TerminalColors.OKBLUE}National collation completed. {collated} records transfered.{TerminalColors.ENDC}')
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
    print(f'{TerminalColors.OKBLUE}Supernational collation completed. {collated} records transfered.{TerminalColors.ENDC}')
    print(':::::::::::::::::::::::::::::::::::::::::::')

    # count the number of parliamentary seats won
    # clear summary sheet
    ParliamentarySummarySheet.objects.all().delete()
    zone_ct = ContentType.objects.get_for_model(Constituency)
    # get all parliamentary positons
    parliamentary_positions = Position.objects.filter(zone_ct=zone_ct).all()
    # get all the canididates for parliamentary positons
    parliamentary_candidates = Candidate.objects.filter(position__in=parliamentary_positions).all()
    # get all results for parliamentary candidates
    results = Result.objects.filter(candidate__in=parliamentary_candidates).all()
    collations = dict()
    for result in results:
        pos_id = result.candidate.position.pk
        can_id = result.candidate.pk
        # extract voting data for position and candidate
        position_collation = collations.get(pos_id, dict())
        votes = position_collation.get(can_id, 0)
        votes += intify(result.votes)
        position_collation[can_id] = votes
        collations[pos_id] = position_collation
    # parse throught the collation sheets
    for kp, position_collations in collations.items():
        max_votes = 0
        total_votes = 0
        max_candidate = None
        for kc, v in position_collations.items():
            # print(kc, kp, v)
            total_votes += v
            if max_votes < v:
                max_votes = v
                max_candidate = kc
        # print(max_votes, max_candidate)
        winning_candidate = Candidate.objects.filter(pk=max_candidate).first()
        position = Position.objects.filter(pk=kp, zone_ct=zone_ct).first()
        constituency = Constituency.objects.filter(pk=position.zone_id).first()
        # create a record for every seat won
        summary, _ = ParliamentarySummarySheet.objects.update_or_create(
            position=position,
            defaults=dict(
                candidate=winning_candidate,
                constituency=constituency,
                votes=max_votes,
                total_votes=total_votes,
            )
        )
        # TODO: To save variances with invalid votes
        print('\t:::::::::::::::::::::::::::::::::::::::::::')
        print(f'\tPosition: {TerminalColors.OKBLUE}{position}{TerminalColors.ENDC}')
        print(f'\tConstituency: {TerminalColors.OKBLUE}{constituency}{TerminalColors.ENDC}')
        print(f'\tWinning candidate {TerminalColors.OKBLUE}{winning_candidate}{TerminalColors.ENDC}')
        print(f'\tVotes: {TerminalColors.OKBLUE}{max_votes}{TerminalColors.ENDC}')

    print(':::::::::::::::::::::::::::::::::::::::::::')

    return total
