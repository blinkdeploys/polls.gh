from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from people.models import Party, Candidate
from people.serializers import PartySerializer
from geo.models import Nation, Region, Constituency, Station
from geo.serializers import RegionSerializer
from poll.forms import OfficeForm
from poll.constants import ROWS_PER_PAGE
from itertools import chain
from django.db.models import Q, Prefetch
from django.db.models import Sum
from poll.utils import snakeify
from poll.constants import StatusChoices, GeoLevelChoices, NameTitleChoices, TerminalColors
from django.db import connection
from poll.models import (
    Event, Office, Position, ResultSheet, Result, ResultApproval,
    SupernationalCollationSheet, NationalCollationSheet, RegionalCollationSheet,
    ConstituencyCollationSheet, StationCollationSheet
)


def get_election_level(level):
    levels = [GeoLevelChoices.CONSTITUENCY, 'parliament', 'parliamentary']
    if level in levels:
        return (GeoLevelChoices.CONSTITUENCY, Constituency, 'Parliamentary', '_parliament')
    return (GeoLevelChoices.NATION, Nation, 'Presidential', '')


def nation_report(request):
    level = GeoLevelChoices.NATIONAL
    level_model = Nation
    report_title = f'National Presidential Collation Results'
    template = f'report/presidential/nation_report.html'
    next_page = 1
    previous_page = 1
    parties = Party.objects.all()
    nation = Nation.objects.first()
    regions = nation.regions.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(zone_ct=ContentType.objects.get_for_model(level_model)) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )
    candidates = None
    for national_position in national_positions:
        position_candidates = national_position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects.filter(
                                                    constituency__in=Constituency.objects.filter(
                                                        region__in=regions
                                                    ).all()
                                                ).all()
                                            ).all(),
                                            to_attr="results_total"
                                        )
                                    )
        for region in regions:
            region_lookup = snakeify(region.title)
            region_lookup = f'results_{region_lookup}'
            # print(region_lookup)
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects \
                                                                .filter(
                                                                        constituency__in=Constituency.objects \
                                                                            .filter(region=region))
                                            ).all(),
                                            to_attr=f"{region_lookup}"
                                        )
                                    )

        if candidates is None:
            candidates = position_candidates
        else:
            candidates = list(chain(candidates, position_candidates))
        

    print(':::::::::::::::::::::::::::::')

    candidate_lists = []
    for candidate in candidates:
        candidate_list = dict()
        candidate_list['pk'] = candidate.pk
        candidate_list['full_name'] = candidate.full_name
        candidate_list['votes'] = candidate.votes
        candidate_list['party'] = candidate.party
        candidate_list['position'] = candidate.position
        for k, v in candidate.__dict__.items():
            if 'results_' in k:
                candidate_list[k] = v
        candidate_lists.append(candidate_list)

        print(candidate_list)
        print('::::::::::::::::::::::::::')

    context = dict(
        title=report_title,
        level=level,
        nation=nation,
        regions=regions,
        parties=parties,
        candidates=candidate_lists,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)


def region_report(request, rpk=None):
    level = GeoLevelChoices.NATIONAL
    level_model = Nation
    report_title = f'Regional Presidential Collation Results'
    template = f'report/presidential/region_report.html'
    next_page = 1
    previous_page = 1
    parties = Party.objects.all()
    region = Region.objects.filter(pk=rpk).first()
    constituencies = region.constituencies.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(zone_ct=ContentType.objects.get_for_model(level_model)) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )
    candidates = None
    for national_position in national_positions:
        position_candidates = national_position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects.filter(
                                                    constituency__in=constituencies
                                                ).all()
                                            ).all(),
                                            to_attr="results_total"
                                        )
                                    )
        for constituency in constituencies:
            constituency_lookup = snakeify(constituency.title)
            constituency_lookup = f'results_{constituency_lookup}'
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                                        station__in=Station.objects \
                                                                                        .filter(constituency=constituency)
                                                                    ).all(),
                                            to_attr=f"{constituency_lookup}"
                                        )
                                    )

        if candidates is None:
            candidates = position_candidates
        else:
            candidates = list(chain(candidates, position_candidates))
        

    print(':::::::::::::::::::::::::::::')

    candidate_lists = []
    for candidate in candidates:
        candidate_list = dict()
        candidate_list['pk'] = candidate.pk
        candidate_list['full_name'] = candidate.full_name
        candidate_list['votes'] = candidate.votes
        candidate_list['party'] = candidate.party
        candidate_list['position'] = candidate.position
        for k, v in candidate.__dict__.items():
            if 'results_' in k:
                candidate_list[k] = v
        candidate_lists.append(candidate_list)

        print(candidate_list)
        print('::::::::::::::::::::::::::')


    context = dict(
        title=report_title,
        level=level,
        region=region,
        constituencies=constituencies,
        parties=parties,
        candidates=candidate_lists,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)


def constituency_report(request, cpk=None):
    level = GeoLevelChoices.NATIONAL
    level_model = Nation
    report_title = f'Constituency Presidential Collation Results'
    template = f'report/presidential/constituency_report.html'
    next_page = 1
    previous_page = 1
    parties = Party.objects.all()
    constituency = Constituency.objects.filter(pk=cpk).first()
    stations = constituency.stations.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(zone_ct=ContentType.objects.get_for_model(level_model)) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )
    candidates = None
    for national_position in national_positions:
        position_candidates = national_position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects \
                                                    .filter(station__in=stations) \
                                                    .all(),
                                            to_attr="results_total"
                                        )
                                    )
        i = 0
        for station in stations:
            station_lookup = snakeify(station.code)
            station_lookup = f'results_{station_lookup}'
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects \
                                                            .filter(station=station) \
                                                            .all(),
                                            to_attr=f"{station_lookup}"
                                        )
                                    )

        if candidates is None:
            candidates = position_candidates
        else:
            candidates = list(chain(candidates, position_candidates))
        

    print(':::::::::::::::::::::::::::::')

    candidate_lists = []
    for candidate in candidates:
        candidate_list = dict()
        candidate_list['pk'] = candidate.pk
        candidate_list['full_name'] = candidate.full_name
        candidate_list['votes'] = candidate.votes
        candidate_list['party'] = candidate.party
        candidate_list['position'] = candidate.position
        for k, v in candidate.__dict__.items():
            if 'results_' in k:
                print(k, '======>', v)
                candidate_list[k] = v
        candidate_lists.append(candidate_list)


    context = dict(
        title=report_title,
        level=level,
        constituency=constituency,
        stations=stations,
        parties=parties,
        candidates=candidate_lists,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)




def nation_parliamentary_report(request):
    template = f'report/parliamentary/nation_report.html'
    report_title = f'National Parliamentary Collation Results'
    level = GeoLevelChoices.CONSTITUENCY
    nation = Nation.objects.first()
    zone_ct = ContentType.objects.get_for_model(Constituency)
    columns = Region.objects.order_by('title').all()

    sums = ''
    sum_joins = ''
    table = 'poll_national_collation_sheet'
    fields = [
        'party_id', 'party_code', 'votes',
    ]
    i = 0
    for column in columns:
        key = f'votes_{snakeify(column.title)}'
        sums += f' SUM(ncs{i}.total_votes) AS {key},'
        sum_joins += f''' LEFT JOIN (
                    SELECT
                            ncs{i}.id,
                            ncs{i}.total_votes
                        FROM {table} ncs{i}
                            LEFT JOIN poll_party p{i} ON p{i}.id = ncs{i}.party_id
                            LEFT JOIN geo_region r{i} ON r{i}.id = ncs{i}.region_id
                        WHERE
                            ncs{i}.zone_ct_id = {zone_ct.pk}
                            AND ncs{i}.region_id = {column.pk}
                        GROUP BY ncs{i}.id, ncs{i}.total_votes
                        ORDER BY ncs{i}.id ASC
                ) AS ncs{i} ON ncs{i}.id = ncs.id
        '''
        fields.append(key)
        i += 1

    query = f'''SELECT
        p.id, p.code,
        SUM(ncs.total_votes) votes,
        {sums}
        '|' AS row_end
    FROM {table} ncs
        LEFT JOIN poll_party p ON p.id = ncs.party_id
        LEFT JOIN geo_region r ON r.id = ncs.region_id
        {sum_joins}
    WHERE
        ncs.zone_ct_id = {zone_ct.pk}
    GROUP BY p.id
    ORDER BY p.code ASC;'''

    reports = []
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            reports.append(dict(zip(fields, row)))
    except Exception as e:
        print("There was an error running raw query", e)


    context = dict(
        title=report_title,
        level=level,
        columns=columns,
        reports=reports,
        zone=nation,
        zone_type='nation',
        sub_zone_type='region',
        sub_zone_type_plural='regions',
        sub_zone_link='/reports/parliamentary/region/',
        # next_link='/poll/offices/?page=' + str(next_page),
        # prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def region_parliamentary_report(request, rpk=None):
    template = f'report/parliamentary/region_report.html'
    report_title = f'Regional Parliamentary Collation Results'
    level = GeoLevelChoices.CONSTITUENCY
    zone_ct = ContentType.objects.get_for_model(Constituency)
    region = Region.objects.filter(pk=rpk).first()
    columns = Constituency.objects.filter(region=region).order_by('title').all()

    sums = ''
    sum_joins = ''
    table = 'poll_regional_collation_sheet'
    fields = [
        'party_id', 'party_code', 'votes',
    ]
    i = 0
    for column in columns:
        key = f'votes_{snakeify(column.title)}'
        sums += f' SUM(ncs{i}.total_votes) AS {key},'
        sum_joins += f''' LEFT JOIN (
                    SELECT
                            ncs{i}.id,
                            ncs{i}.total_votes
                        FROM {table} ncs{i}
                            LEFT JOIN poll_party p{i} ON p{i}.id = ncs{i}.party_id
                            LEFT JOIN geo_constituency c{i} ON c{i}.id = ncs{i}.constituency_id
                            LEFT JOIN geo_region r{i} ON r{i}.id = c{i}.region_id
                        WHERE
                            ncs{i}.zone_ct_id = {zone_ct.pk}
                            AND ncs{i}.constituency_id = {column.pk}
                            AND r{i}.id = {rpk}
                        GROUP BY ncs{i}.id, ncs{i}.total_votes
                        ORDER BY ncs{i}.id ASC
                ) AS ncs{i} ON ncs{i}.id = ncs.id
        '''
        fields.append(key)
        i += 1

    query = f'''SELECT
        p.id, p.code,
        SUM(ncs.total_votes) votes,
        {sums}
        '|' AS row_end
    FROM {table} ncs
        LEFT JOIN poll_party p ON p.id = ncs.party_id
        LEFT JOIN geo_constituency c ON c.id = ncs.constituency_id
        LEFT JOIN geo_region r ON r.id = c.region_id
        {sum_joins}
    WHERE
        ncs.zone_ct_id = {zone_ct.pk}
        AND r.id = {rpk}
    GROUP BY p.id
    ORDER BY p.code ASC;'''

    reports = []
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            reports.append(dict(zip(fields, row)))
    except Exception as e:
        print("There was an error running raw query", e)


    context = dict(
        title=report_title,
        level=level,
        columns=columns,
        reports=reports,
        zone=region,
        sub_zone_link='/reports/parliamentary/constituency/',
        zone_type='region',
        sub_zone_type='constituency',
        sub_zone_type_plural='constituencies',
        # next_link='/poll/offices/?page=' + str(next_page),
        # prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def constituency_parliamentary_report(request, cpk=None):
    template = f'report/parliamentary/constituency_report.html'
    report_title = f'Constituency Parliamentary Collation Results'
    level = GeoLevelChoices.CONSTITUENCY
    zone_ct = ContentType.objects.get_for_model(Constituency)
    constituency = Constituency.objects.filter(pk=cpk).first()
    columns = Station.objects.filter(constituency=constituency).order_by('code').all()

    sums = ''
    sum_joins = ''
    table = 'poll_constituency_collation_sheet'
    fields = [
        'party_id', 'party_code', 'votes',
    ]
    i = 0
    for column in columns:
        key = f'votes_{snakeify(column.title)}'
        sums += f' SUM(ncs{i}.total_votes) AS {key},'
        sum_joins += f''' LEFT JOIN (
                    SELECT
                            ncs{i}.id,
                            ncs{i}.total_votes
                        FROM {table} ncs{i}
                            LEFT JOIN poll_party p{i} ON p{i}.id = ncs{i}.party_id
                            LEFT JOIN geo_station s{i} ON s{i}.id = ncs{i}.station_id
                            LEFT JOIN geo_constituency c{i} ON c{i}.id = s{i}.constituency_id
                            LEFT JOIN geo_region r{i} ON r{i}.id = c{i}.region_id
                        WHERE
                            ncs{i}.zone_ct_id = {zone_ct.pk}
                            AND ncs{i}.station_id = {column.pk}
                            AND c{i}.id = {cpk}
                        GROUP BY ncs{i}.id, ncs{i}.total_votes
                        ORDER BY ncs{i}.id ASC
                ) AS ncs{i} ON ncs{i}.id = ncs.id
        '''
        fields.append(key)
        i += 1

    query = f'''SELECT
        p.id, p.code,
        SUM(ncs.total_votes) votes,
        {sums}
        '|' AS row_end
    FROM {table} ncs
        LEFT JOIN poll_party p ON p.id = ncs.party_id
        LEFT JOIN geo_station s ON s.id = ncs.station_id
        LEFT JOIN geo_constituency c ON c.id = s.constituency_id
        LEFT JOIN geo_region r ON r.id = c.region_id
        {sum_joins}
    WHERE
        ncs.zone_ct_id = {zone_ct.pk}
        AND c.id = {cpk}
    GROUP BY p.id
    ORDER BY p.code ASC;'''

    reports = []
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            reports.append(dict(zip(fields, row)))
    except Exception as e:
        print("There was an error running raw query", e)


    context = dict(
        title=report_title,
        level=level,
        columns=columns,
        reports=reports,
        zone=constituency,
        sub_zone_link='/reports/parliamentary/station/',
        zone_type='constituency',
        sub_zone_type='station',
        # next_link='/poll/offices/?page=' + str(next_page),
        # prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def station_parliamentary_report(request, spk=None):
    template = f'report/parliamentary/station_report.html'
    report_title = f'Station Parliamentary Collation Results'
    level = GeoLevelChoices.CONSTITUENCY
    zone_ct = ContentType.objects.get_for_model(Constituency)
    station = Station.objects.filter(pk=spk).first()
    columns = [] # Station.objects.filter(constituency=constituency).order_by('code').all()

    sums = ''
    sum_joins = ''
    table = 'poll_station_collation_sheet'
    fields = [
        'party_id', 'party_code', 'votes',
    ]
    
    fields += ['candidate_name']
    select_candidate_name = " CONCAT(ca.prefix, ' ', ca.first_name, ' ', ca.last_name) candidate_name,"
    group_candidate_name = ', ca.prefix, ca.first_name, ca.last_name'

    i = 0
    for column in columns:
        key = f'votes_{snakeify(column.title)}'
        sums += f' SUM(ncs{i}.total_votes) AS {key},'
        sum_joins += f''' LEFT JOIN (
                    SELECT
                            ncs{i}.id,
                            ncs{i}.total_votes
                        FROM {table} ncs{i}
                            LEFT JOIN poll_party p{i} ON p{i}.id = ncs{i}.party_id
                            LEFT JOIN geo_station s{i} ON s{i}.id = ncs{i}.station_id
                            LEFT JOIN geo_constituency c{i} ON c{i}.id = s{i}.constituency_id
                            LEFT JOIN geo_region r{i} ON r{i}.id = c{i}.region_id
                        WHERE
                            ncs{i}.zone_ct_id = {zone_ct.pk}
                            AND ncs{i}.station_id = {column.pk}
                            AND c{i}.id = {cpk}
                        GROUP BY ncs{i}.id, ncs{i}.total_votes
                        ORDER BY ncs{i}.id ASC
                ) AS ncs{i} ON ncs{i}.id = ncs.id
        '''
        fields.append(key)
        i += 1

    query = f'''SELECT
        p.id, p.code,
        SUM(ncs.total_votes) votes,
        {sums}
        {select_candidate_name}
        '|' AS row_end
    FROM {table} ncs
        LEFT JOIN people_candidate ca ON ca.id = ncs.candidate_id
        LEFT JOIN poll_party p ON p.id = ca.party_id
        LEFT JOIN geo_station s ON s.id = ncs.station_id
        LEFT JOIN geo_constituency c ON c.id = s.constituency_id
        LEFT JOIN geo_region r ON r.id = c.region_id
        {sum_joins}
    WHERE
        ncs.zone_ct_id = {zone_ct.pk}
        AND s.id = {spk}
    GROUP BY p.id
        {group_candidate_name}
    ORDER BY p.code ASC;'''

    reports = []
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            reports.append(dict(zip(fields, row)))
    except Exception as e:
        print("There was an error running raw query", e)

    context = dict(
        title=report_title,
        level=level,
        columns=columns,
        reports=reports,
        zone=station,
        sub_zone_link='#',
        zone_type='station',
        sub_zone_type=None,
        # next_link='/poll/offices/?page=' + str(next_page),
        # prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)



def nation_parliamentary_report_2(request):
    level = GeoLevelChoices.CONSTITUENCY
    level_model = Constituency
    report_title = f'National Parliamentary Collation Results'
    template = f'report/parliamentary/nation_report.html'
    next_page = 1
    previous_page = 1
    parties = Party.objects.all()
    nation = Nation.objects.first()
    regions = nation.regions.all()


    '''
    positions = Position.objects.filter(
        zone_ct=ContentType.objects.get_for_model(Constituency)
    ).all()
    parties = Party.objects.prefetch_related(
        Prefetch(
            'candidates',
            queryset=Candidate.objects.filter(
                position__in=positions
            ).prefetch_related('results').all(),
            to_attr='party_candidates'
        )
    ).all()

    totals = dict()
    for party in parties:
        for candidate in party.candidates.all():
            for result in candidate.results.all():
                print(':::::::::::::::::::::::')
                if totals.get(party.code, None) is None:
                    totals[party.code] = dict()
                totals[party.code]['votes']
                totals[party.code]['votes']
                print(
                    result.votes, result.candidate,
                    result.result_sheet.station.title)
        totals.append(total)

    print(':::::::::::::::::::::::')
    '''
    query = '''SELECT
            p.id, p.code, p.title,
            COUNT(c.id) candidates,
            COUNT(r.id) results,
            COUNT(rs.id) result_sheets,
            SUM(r.votes) votes
        FROM poll_party p
            LEFT JOIN people_candidate c ON c.party_id = p.id
            LEFT JOIN poll_result r ON r.candidate_id = c.id
            LEFT JOIN poll_position po ON po.id = c.position_id AND po.zone_ct_id = '9'
            LEFT JOIN poll_result_sheet rs ON rs.position_id = c.position_id AND r.result_sheet_id = rs.id
        GROUP BY p.id;'''


    query = '''SELECT
    p.id, p.code, p.title,
    COUNT(c.id) candidates,
    COUNT(rs.id) result_sheets,
    COUNT(r.id) results,
    SUM(r.votes) votes
FROM poll_party p
    LEFT JOIN people_candidate c ON c.party_id = p.id
    LEFT JOIN poll_position po ON po.id = c.position_id
    LEFT JOIN poll_result_sheet rs ON rs.position_id = po.id AND rs.position_id = c.position_id
    LEFT JOIN poll_result r ON r.result_sheet_id = rs.id AND r.candidate_id = c.id
    LEFT JOIN geo_station s ON s.id = rs.station_id AND s.id = r.station_id
WHERE
    po.zone_ct_id = '9'
    AND po.id = '1639'
    AND s.id = '1'
    -- AND po.zone_id = '48'
GROUP BY p.id
ORDER BY votes DESC
;
    '''


    




    '''
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(zone_ct=ContentType.objects.get_for_model(level_model)) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )
    candidates = None
    for national_position in national_positions:
        position_candidates = national_position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects.filter(
                                                    constituency__in=Constituency.objects.filter(
                                                        region__in=regions
                                                    ).all()
                                                ).all()
                                            ).all(),
                                            to_attr="results_total"
                                        )
                                    )
        for region in regions:
            region_lookup = snakeify(region.title)
            region_lookup = f'results_{region_lookup}'
            # print(region_lookup)
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects \
                                                                .filter(
                                                                        constituency__in=Constituency.objects \
                                                                            .filter(region=region))
                                            ).all(),
                                            to_attr=f"{region_lookup}"
                                        )
                                    )

        if candidates is None:
            candidates = position_candidates
        else:
            candidates = list(chain(candidates, position_candidates))
        

    print(':::::::::::::::::::::::::::::')

    candidate_lists = []
    for candidate in candidates:
        candidate_list = dict()
        candidate_list['pk'] = candidate.pk
        candidate_list['full_name'] = candidate.full_name
        candidate_list['votes'] = candidate.votes
        candidate_list['party'] = candidate.party
        candidate_list['position'] = candidate.position
        for k, v in candidate.__dict__.items():
            if 'results_' in k:
                candidate_list[k] = v
        candidate_lists.append(candidate_list)

        print(candidate_list)
        print('::::::::::::::::::::::::::')
    '''




    
    cursor = connection.cursor()
    zone_ct = ContentType.objects.get_for_model(Constituency)
    
    sums = ''
    sum_joins = ''
    stations = Station.objects.all()[100:200]
    fields = ['pk', 'party_code', 'party_title',
              'candidate', 'won', 'result_sheets',
              'results', 'results_total', 'max_result']
    i = 0
    columns = stations

    group_by = 'c.id, p.id'
    # if collapse to party
        # group_by = 'p.id'

    cid = 1
    constituency = Constituency.objects.filter(pk=cid).first()
    position = Position.objects.filter(
        zone_ct=zone_ct,
        zone_id=constituency.pk
    ).first()

    append = '_max'
    sum_joins += f''' LEFT JOIN (SELECT
                    r{append}.result_sheet_id,
                    r{append}.candidate_id,
                    SUM(r{append}.votes) total_votes
                FROM poll_party p{append}
                    LEFT JOIN people_candidate c{append} ON c{append}.party_id = p{append}.id
                    LEFT JOIN poll_position po{append} ON po{append}.id = c{append}.position_id
                        AND po{append}.id = '{position.pk}'
                    LEFT JOIN poll_result_sheet rs{append} ON rs{append}.position_id = po{append}.id AND rs{append}.position_id = c{append}.position_id
                    LEFT JOIN poll_result r{append} ON r{append}.result_sheet_id = rs{append}.id AND r{append}.candidate_id = c{append}.id
                    LEFT JOIN geo_station s{append} ON s{append}.id = rs{append}.station_id AND s{append}.id = r{append}.station_id
                        AND s{append}.constituency_id = '{constituency.pk}'
                WHERE
                    po{append}.zone_ct_id = '{zone_ct.pk}'
                GROUP BY r{append}.id
                ORDER BY votes DESC
            ) AS r{append} ON
                    r{append}.result_sheet_id = rs.id
                    AND r{append}.candidate_id = c.id'''

    for station in stations:
        fields.append(snakeify(f'results_{station.code}'))
        sums += f''' SUM(r{i}.votes) as votes{i},'''
        sum_joins += f''' LEFT JOIN (SELECT
                    r{i}.*
                FROM poll_party p{i}
                    LEFT JOIN people_candidate c{i} ON c{i}.party_id = p{i}.id
                    LEFT JOIN poll_position po{i} ON po{i}.id = c{i}.position_id
                        AND po{i}.id = '{position.pk}'
                    LEFT JOIN poll_result_sheet rs{i} ON rs{i}.position_id = po{i}.id AND rs{i}.position_id = c{i}.position_id
                    LEFT JOIN poll_result r{i} ON r{i}.result_sheet_id = rs{i}.id AND r{i}.candidate_id = c{i}.id
                    LEFT JOIN geo_station s{i} ON s{i}.id = rs{i}.station_id AND s{i}.id = r{i}.station_id
                        AND s{i}.constituency_id = '{constituency.pk}'
                WHERE
                    po{i}.zone_ct_id = '{zone_ct.pk}'
                    AND s{i}.constituency_id = '{station.constituency_id}'
                    AND s{i}.id = '{station.pk}'
                GROUP BY r{i}.id
                ORDER BY votes DESC
            ) AS r{i} ON r{i}.result_sheet_id = rs.id AND r{i}.candidate_id = c.id'''
        i += 1


    query = f'''SELECT
                p.id, p.code, p.title,
                CONCAT(c.prefix, c.first_name, ' ', c.last_name),
                (CASE WHEN (SUM(r.votes) > 0 AND SUM(r.votes) = MAX(r{append}.total_votes)) THEN 1 ELSE 0 END) won,

                COUNT(rs.id) result_sheets,
                COUNT(r.id) results,

                SUM(r.votes) votes,
                MAX(r{append}.total_votes) max_votes,

                {sums}

                '|' AS end_row

            FROM poll_party p

                LEFT JOIN people_candidate c ON c.party_id = p.id
                LEFT JOIN poll_position po ON po.id = c.position_id
                LEFT JOIN poll_result_sheet rs ON rs.position_id = po.id AND rs.position_id = c.position_id
                LEFT JOIN poll_result r ON r.result_sheet_id = rs.id AND r.candidate_id = c.id
                LEFT JOIN geo_station s ON s.id = rs.station_id AND s.id = r.station_id

                {sum_joins}
                
            WHERE
                po.zone_ct_id = '{zone_ct.pk}'
                -- AND po.id = '1639'
                AND po{i}.id = '{position.pk}'
                -- AND s.constituency_id = '258'
            GROUP BY {group_by}
            ORDER BY won DESC, votes DESC
                -- , p.id ASC
            -- LIMIT 500
            ;'''

    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")
    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")
    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")
    reports = []
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            reports.append(dict(zip(fields, row)))
    except Exception as e:
        print("There was an error running raw query", e)
    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")
    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")
    # print("*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*:*")

    # from pprint import pprint
    # pprint(report)


    context = dict(
        title=report_title,
        level=level,
        nation=nation,
        regions=regions,
        parties=parties,

        reports=reports,
        columns=columns,

        # candidates=candidate_lists,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def region_parliamentary_report_2(request, rpk=None):
    level = GeoLevelChoices.CONSTITUENCY
    level_model = Constituency
    report_title = f'Regional Parliamentary Collation Results'
    template = f'report/parliamentary/region_report.html'
    next_page = 1
    previous_page = 1
    parties = Party.objects.all()
    region = Region.objects.filter(pk=rpk).first()
    constituencies = region.constituencies.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(
                                    zone_ct=ContentType.objects.get_for_model(level_model),
                                    zone_id__in=constituencies
                                ) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )
    candidates = None
    for national_position in national_positions:
        position_candidates = national_position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                station__in=Station.objects.filter(
                                                    constituency__in=constituencies
                                                ).all()
                                            ).all(),
                                            to_attr="results_total"
                                        )
                                    )
        for constituency in constituencies:
            constituency_lookup = snakeify(constituency.title)
            constituency_lookup = f'results_{constituency_lookup}'
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects.filter(
                                                                        station__in=Station.objects \
                                                                                        .filter(constituency=constituency)
                                                                    ).all(),
                                            to_attr=f"{constituency_lookup}"
                                        )
                                    )

        if candidates is None:
            candidates = position_candidates
        else:
            candidates = list(chain(candidates, position_candidates))
        
    print(':::::::::::::::::::::::::::::')

    candidate_lists = []
    for candidate in candidates:
        candidate_list = dict()
        candidate_list['pk'] = candidate.pk
        candidate_list['full_name'] = candidate.full_name
        candidate_list['votes'] = candidate.votes
        candidate_list['party'] = candidate.party
        candidate_list['position'] = candidate.position
        candidate_list['position_title'] = candidate.position.title
        candidate_list['position_id'] = candidate.position.pk
        for k, v in candidate.__dict__.items():
            if 'results_' in k:
                candidate_list[k] = v
        candidate_lists.append(candidate_list)

        print(candidate_list)
        print('::::::::::::::::::::::::::')


    context = dict(
        title=report_title,
        level=level,
        region=region,
        constituencies=constituencies,
        parties=parties,
        candidates=candidate_lists,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def constituency_parliamentary_report_2(request, cpk=None):
    level = GeoLevelChoices.CONSTITUENCY
    level_model = Constituency
    report_title = f'Constituency Parliamentary Collation Results'
    template = f'report/parliamentary/constituency_report.html'
    next_page = 1
    previous_page = 1
    candidate_lists = []
    parties = []
    constituency = None
    stations = []

    # try:
    parties = Party.objects.all()
    constituency = Constituency.objects.filter(pk=cpk).first()
    stations = constituency.stations.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.filter(
                                        station__in=stations
                                    ).all(),
                                    to_attr="results_total"
                                )
                            )

    national_positions = Position.objects \
                                .filter(
                                    zone_ct=ContentType.objects.get_for_model(level_model),
                                    zone_id=constituency.pk
                                ) \
                                .prefetch_related(
                                    Prefetch(
                                        'candidates',
                                        to_attr='position_candidates',
                                        queryset=candidate_qs
                                    )
                                )

    # print(":::::::::::::::::::::::::::::")
    # print(national_positions.count())
    # print(":::::::::::::::::::::::::::::")

    candidates = []
    for position in national_positions:
        position_candidates = position.candidates.all() \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects \
                                                    .filter(station__in=stations) \
                                                    .all(),
                                            to_attr="results_total"
                                        )
                                    )
        print(":::::::::::::::::::::::::::::")
        print(position_candidates.count())
        print(":::::::::::::::::::::::::::::")

        for candidate in position_candidates:
            candidate_dict = dict(
                pk=candidate.pk,
                full_name=candidate.full_name,
                position_id=position.pk,
                position_title=position.title,
                votes=candidate.votes,
                party=candidate.party,
                position=candidate.position,
            )
            candidates.append(candidate_dict)

        for station in stations:
            station_lookup = snakeify(station.code)
            station_lookup = f'results_{station_lookup}'
            position_candidates = position_candidates \
                                    .prefetch_related(
                                        Prefetch(
                                            'results',
                                            queryset=Result.objects \
                                                            .filter(station=station) \
                                                            .all(),
                                            to_attr=f"{station_lookup}"
                                        )
                                    )
            print(position_candidates.count())
            c = 0
            for candidate in position_candidates:
                for k, v in candidate.__dict__.items():
                    if 'results_' in k:
                        print(k, '======>', v)
                        total = candidate_dict.get(k, 0)
                        candidates[c][k] = v if total == 0 else total + v
                c += 1


    print(':::::::::::::::::::::::::::::')


    # except Exception as e:
    #     print('There was an error fetching records', e)


    context = dict(
        title=report_title,
        level=level,
        constituency=constituency,
        stations=stations,
        parties=parties,
        candidates=candidates,
        next_link='/poll/offices/?page=' + str(next_page),
        prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)

def station_parliamentary_report_2(request, spk=None):
    level = GeoLevelChoices.CONSTITUENCY
    level_model = Constituency
    report_title = f'Polling Station Parliamentary Collation Results'
    template = f'report/parliamentary/station_report.html'


    '''
    next_page = 1
    previous_page = 1
    candidates = []
    parties = Party.objects.all()
    station = Station.objects.filter(pk=spk).first()
    # stations = constituency.stations.all()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects \
                                            .filter(station=station) \
                                            .all(),
                                    to_attr="results_total"
                                )
                            )

    positions = Position.objects \
                        .filter(
                            zone_ct=ContentType.objects.get_for_model(level_model),
                            zone_id=station.constituency.pk
                        ) \
                        .prefetch_related(
                            Prefetch(
                                'candidates',
                                to_attr='position_candidates',
                                queryset=candidate_qs
                            )
                        )

    print(':::::::::::::::::::::::::::::')

    for position in positions:
        position_candidates = position.candidates.all()
        for candidate in position_candidates:
            candidate_dict = dict(
                pk=candidate.pk,
                position_id=position.pk,
                position_title=position.title,
                full_name=candidate.full_name,
                votes=candidate.votes,
                party=candidate.party,
                position=candidate.position
            )
            for k, v in candidate.__dict__.items():
                if 'results_' in k:
                    print(k, '======>', v)
                    candidate_dict[k] = v
            candidates.append(candidate_dict)
    '''






    context = dict(
        title=report_title,
        level=level,
        station=station,
        # parties=parties,
        # candidates=candidates,
        # next_link='/poll/offices/?page=' + str(next_page),
        # prev_link='/poll/offices/?page=' + str(previous_page)
    )
    return render(request, template, context)
