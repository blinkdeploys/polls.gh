from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from poll.models import Position, Result
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


def nation_report(request):
    nextPage = 1
    previousPage = 1
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
                                .filter(zone_ct=ContentType.objects.get_for_model(Nation)) \
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

    context = {
        'title': 'National Presidential Collation Results',
        'nation': nation,
        'regions': regions,
        'parties': parties,
        'candidates': candidate_lists,
        'next_link': '/poll/offices/?page=' + str(nextPage),
        'prev_link': '/poll/offices/?page=' + str(previousPage)
    }
    return render(request, "report/nation_report.html", context)


def region_report(request, rpk=None):
    nextPage = 1
    previousPage = 1
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
                                .filter(zone_ct=ContentType.objects.get_for_model(Nation)) \
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


    context = {
        'title': 'Regional Presidential Collation Results',
        'region': region,
        'constituencies': constituencies,
        'parties': parties,
        'candidates': candidate_lists,
        'next_link': '/poll/offices/?page=' + str(nextPage),
        'prev_link': '/poll/offices/?page=' + str(previousPage)
    }
    return render(request, "report/region_report.html", context)


def constituency_report(request, cpk=None):
    nextPage = 1
    previousPage = 1
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
                                .filter(zone_ct=ContentType.objects.get_for_model(Nation)) \
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


    context = {
        'title': 'Constituency Presidential Collation Results',
        'constituency': constituency,
        'stations': stations,
        'parties': parties,
        'candidates': candidate_lists,
        'next_link': '/poll/offices/?page=' + str(nextPage),
        'prev_link': '/poll/offices/?page=' + str(previousPage)
    }
    return render(request, "report/constituency_report.html", context)

