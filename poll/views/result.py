import io
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from geo.models import Station, Nation, Constituency
from poll.models import ResultSheet, Result, Position
from people.models import Party, Candidate
from poll.serializers import ResultSerializer, PositionSerializer
from geo.serializers import StationSerializer
from people.serializers import PartySerializer, CandidateSerializer
from django.contrib.contenttypes.models import ContentType
from poll.forms import ResultForm
from poll.constants import ROWS_PER_PAGE
from django.db.models import Q, Prefetch
from poll.constants import StatusChoices
from django.contrib import messages


def result_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    
    result = Result.objects.all()
    # stations = Station.objects.all()
    # candidates = Candidate.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(result, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = ResultSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()


    context = {
        'title': 'Results',
        'data': serializer.data,
        # 'candidates': candidates.data,
        # 'count': paginator.count,
        # 'numpages' : paginator.num_pages,
        # 'columns': ['candidate_details', 'station.title', 'votes', 'constituency_agent', 'result_sheet'],
        # 'next_link': '/poll/results/?page=' + str(nextPage),
        # 'prev_link': '/poll/results/?page=' + str(previousPage)
    }
    template = "poll/result_list.html"
    return render(request, template, context)

def station_list(request):
    data = []
    station_next_page = 1
    station_previous_page = 1
    total_per_page = ROWS_PER_PAGE
    q = request.GET.get('q', '')
    station_page = request.GET.get('spage', 1)
    base_url = '/poll/result/stations?'
    if len(q) > 0:
        base_url = f'{base_url}q={q}'
    
    # result = Result.objects.first()
    stations = Station.objects \
                      .filter(Q(title__icontains=q) | Q(code__icontains=q)) \
                      .all()
    # candidates = Candidate.objects.all()

    # paginator = Paginator(result, total_per_page)
    # try:
    #     data = paginator.page(page)
    # except PageNotAnInteger:
    #     data = paginator.page(1)
    # except EmptyPage:
    #     data = paginator.page(paginator.num_pages)

    # serializer = ResultSerializer(data, context={'request': request}, many=True)
    # if data.has_next():
    #     nextPage = data.next_page_number()
    # if data.has_previous():
    #     previousPage = data.previous_page_number()

    station_page = request.GET.get('spage', 1)
    station_paginator = Paginator(stations, total_per_page)
    try:
        station_data = station_paginator.page(station_page)
    except PageNotAnInteger:
        station_data = station_paginator.page(1)
    except EmptyPage:
        station_data = station_paginator.page(station_paginator.num_pages)

    station_serializer = StationSerializer(station_data, context={'request': request}, many=True)

    if station_data.has_next():
        station_next_page = station_data.next_page_number()
    if station_data.has_previous():
        station_previous_page = station_data.previous_page_number()


    context = {
        'title': 'Results',
        # 'data': serializer.data,
        'stations': station_serializer.data,
        'q': q,
        # 'candidates': candidates.data,
        # 'columns': ['candidate_details', 'station.title', 'votes', 'constituency_agent', 'result_sheet'],
        'station_numpages' : station_paginator.num_pages,
        'station_count': station_paginator.count,
        'station_next_link': f'{base_url}&spage=' + str(station_next_page),
        'station_prev_link': f'{base_url}&spage=' + str(station_previous_page)
    }
    template = "poll/result_list.html"
    return render(request, template, context)

def position_list(request, spk=None):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    
    nation = Nation.objects.first()
    stations = Station.objects.filter(pk=spk)

    constituency = stations.first().constituency

    positions = Position.objects.filter(
        zone_ct__in=[ContentType.objects.get_for_model(Nation), 
                     ContentType.objects.get_for_model(Constituency)],
        zone_id__in=[nation.pk, constituency.pk]
    )
    presidential_positions = Position.objects.filter(
        zone_ct=ContentType.objects.get_for_model(Nation),
        zone_id=nation.pk
    )
    parliamentary_positions = Position.objects.filter(
        zone_ct=ContentType.objects.get_for_model(Constituency),
        zone_id=constituency.pk
    )
    position_ids = [p.pk for p in presidential_positions] + [p.pk for p in parliamentary_positions]
    positions = Position.objects.filter(
        pk__in=position_ids
    )

    station_page = request.GET.get('spage', 1)
    station_paginator = Paginator(stations, total_per_page)
    try:
        station_data = station_paginator.page(station_page)
    except PageNotAnInteger:
        station_data = station_paginator.page(1)
    except EmptyPage:
        station_data = station_paginator.page(station_paginator.num_pages)
    station_serializer = StationSerializer(station_data, context={'request': request}, many=True)

    position_page = request.GET.get('spage', 1)
    position_paginator = Paginator(positions, total_per_page)
    try:
        position_data = position_paginator.page(position_page)
    except PageNotAnInteger:
        position_data = position_paginator.page(1)
    except EmptyPage:
        position_data = position_paginator.page(position_paginator.num_pages)
    position_serializer = PositionSerializer(position_data, context={'request': request}, many=True)

    context = {
        'title': 'Results',
        # 'data': serializer.data,
        'stations': station_serializer.data,
        'positions': position_serializer.data,
        # 'candidates': candidates.data,
        # 'count': paginator.count,
        # 'numpages' : paginator.num_pages,
        # 'columns': ['candidate_details', 'station.title', 'votes', 'constituency_agent', 'result_sheet'],
        # 'next_link': '/poll/results/?page=' + str(nextPage),
        # 'prev_link': '/poll/results/?page=' + str(previousPage)
    }
    template = "poll/result_list.html"
    return render(request, template, context)

def candidate_list(request, spk=None, ppk=None):
    messages.get_messages(request)
    template = "poll/result_list.html"
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    
    nation = Nation.objects.first()
    stations = Station.objects.filter(pk=spk)

    constituency = stations.first().constituency

    presidential_positions = Position.objects.filter(
        zone_ct=ContentType.objects.get_for_model(Nation),
        zone_id=nation.pk,
        pk=ppk
    )
    parliamentary_positions = Position.objects.filter(
        zone_ct=ContentType.objects.get_for_model(Constituency),
        zone_id=constituency.pk,
        pk=ppk
    )
    position_ids = [p.pk for p in presidential_positions] + [p.pk for p in parliamentary_positions]
    positions = Position.objects.filter(
        pk__in=position_ids
    )

    candidates = Candidate.objects \
                          .filter(position_id__in=[p.pk for p in positions]) \
                          .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.filter(station_id=spk),
                                    to_attr="station_results"
                                )
                          )
    
    result_sheet = ResultSheet.objects \
                            .filter(station__in=stations, position__in=positions) \
                            .first()
    result_sheet_url = None
    if result_sheet.result_sheet:
        result_sheet_url = request.build_absolute_uri(result_sheet.result_sheet.url)

    parties = Party.objects \
                    .prefetch_related(
                        Prefetch(
                            'candidates',
                            queryset=Candidate.objects \
                                .filter(position=ppk)
                                .prefetch_related(
                                    Prefetch(
                                        'results',
                                        queryset=Result.objects.filter(station_id=spk),
                                        to_attr="station_results"
                                    )
                                ),
                            to_attr="party_candidates"
                        )
                    )

    # results = Result.objects.filter(
    #     candidate__in=candidates,
    #     station__in=stations
    # )

    station_page = request.GET.get('spage', 1)
    station_paginator = Paginator(stations, total_per_page)
    try:
        station_data = station_paginator.page(station_page)
    except PageNotAnInteger:
        station_data = station_paginator.page(1)
    except EmptyPage:
        station_data = station_paginator.page(station_paginator.num_pages)
    station_serializer = StationSerializer(station_data, context={'request': request}, many=True)

    position_page = request.GET.get('ppage', 1)
    position_paginator = Paginator(positions, total_per_page)
    try:
        position_data = position_paginator.page(position_page)
    except PageNotAnInteger:
        position_data = position_paginator.page(1)
    except EmptyPage:
        position_data = position_paginator.page(station_paginator.num_pages)
    position_serializer = PositionSerializer(position_data, context={'request': request}, many=True)

    candidate_page = request.GET.get('cpage', 1)
    candidate_paginator = Paginator(candidates, total_per_page)
    try:
        candidate_data = candidate_paginator.page(candidate_page)
    except PageNotAnInteger:
        candidate_data = candidate_paginator.page(1)
    except EmptyPage:
        candidate_data = candidate_paginator.page(candidate_paginator.num_pages)
    candidate_serializer = CandidateSerializer(candidate_data, context={'request': request}, many=True)

    party_page = request.GET.get('papage', 1)
    party_paginator = Paginator(parties, total_per_page)
    try:
        party_data = party_paginator.page(party_page)
    except PageNotAnInteger:
        party_data = party_paginator.page(1)
    except EmptyPage:
        party_data = party_paginator.page(party_paginator.num_pages)
    party_serializer = CandidateSerializer(party_data, context={'request': request}, many=True)

    # result_page = request.GET.get('spage', 1)
    # result_paginator = Paginator(results, total_per_page)
    # try:
    #     result_data = result_paginator.page(result_page)
    # except PageNotAnInteger:
    #     result_data = result_paginator.page(1)
    # except EmptyPage:
    #     result_data = result_paginator.page(result_paginator.num_pages)
    # result_serializer = ResultSerializer(result_data, context={'request': request}, many=True)

    context = {
        'title': 'Results',
        # 'data': serializer.data,
        # 'results': result_serializer.data,
        'stations': station_serializer.data,
        'positions': position_serializer.data,
        # 'candidates': candidate_data, # candidate_serializer.data,
        'parties': party_data,
        'result_sheet': result_sheet,
        'result_sheet_url': result_sheet_url,
        'spk': spk,
        'ppk': ppk,
        # 'count': paginator.count,
        # 'numpages' : paginator.num_pages,
        # 'columns': ['candidate_details', 'station.title', 'votes', 'constituency_agent', 'result_sheet'],
        # 'next_link': '/poll/results/?page=' + str(nextPage),
        # 'prev_link': '/poll/results/?page=' + str(previousPage)
    }
    if request.method == 'POST':
        print("*********************************")
        from pprint import pprint
        # pprint(request.POST.__dict__)
        # pprint(request.POST.getlist('votes'))
        pprint(request.POST.getlist('candidate'))
        # pprint(request.POST.get('station', 0))
        pprint(request.FILES['result_sheet'])

        station = request.POST.get('station', 0)
        position = request.POST.get('position', 0)
        total_votes = request.POST.get('total_votes', 0)
        total_invalid_votes = request.POST.get('total_invalid_votes', 0)
        total_valid_votes = request.POST.get('total_valid_votes', 0)
        result_sheet_file = request.FILES['result_sheet']

        candidates = request.POST.getlist('candidate', [])
        votes = request.POST.getlist('votes', [])

        station = 0 if len(station) <= 0 else int(station)
        position = 0 if len(position) <= 0 else int(position)
        total_votes = 0 if len(total_votes) <= 0 else int(total_votes)
        total_invalid_votes = 0 if len(total_invalid_votes) <= 0 else int(total_invalid_votes)
        total_valid_votes = 0 if len(total_valid_votes) <= 0 else int(total_valid_votes)

        n = len(candidates)

        result_sheet, _ = ResultSheet.objects.update_or_create(
                                    station_id=station,
                                    position_id=position,
                                    defaults=dict(
                                        total_votes=total_votes,
                                        total_valid_votes=total_valid_votes,
                                        total_invalid_votes=total_invalid_votes,
                                        result_sheet=result_sheet_file,
                                        station_agent=None,
                                        station_approval_at=None,
                                        constituency_agent=None,
                                        constituency_approved_at=None,
                                        region_agent=None,
                                        regional_approval_at=None,
                                        nation_agent=None,
                                        national_approval_at=None,
                                        status=StatusChoices.ACTIVE
                                    )
        )


        for i in range(0, n):
            try:
                result_vote = 0 if len(votes[i]) <= 0 else int(votes[i])
                result_candidate = 0 if len(candidates[i]) <= 0 else int(candidates[i])
                result, _ = Result.objects.update_or_create(
                                            station_id=station,
                                            candidate_id=result_candidate,
                                            defaults=dict(
                                                votes=result_vote,
                                                result_sheet=result_sheet,
                                                station_agent=None,
                                                status=StatusChoices.ACTIVE
                                            )
                                        )
            except Exception as e:
                print(e)
                context = {
                    'error': 'There was an error saving the result. Please try again.'
                }
        print("*********************************")
        message="Result sheet successfully saved"
        context = {
            'message': message
        }
        messages.success(request, message)
        return redirect(reverse('result_candidate_list', kwargs=dict(spk=spk, ppk=ppk)), "Result sheet successfully saved")
    return render(request, template, context)

def result_detail(request, pk=None):
    data = get_object_or_404(Result, pk=pk)
    initial = {
        'pk': data.pk,
        'constituency_agent': data.constituency_agent,
        'candidate': data.candidate,
        'station': data.station,
        'votes': data.votes,
        'result_sheet': data.result_sheet,
        'status': data.status,
    }
    if request.method == "GET":
        form = ResultForm(initial=initial)
    else:
        form = ResultForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            result = form.cleaned_data['result']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                result = Result(code=code, title=title, result=result)
                result.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "poll/result_form.html", {"form": form})


def success_view(request):
    form = ResultForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "poll/result_form.html", context)


