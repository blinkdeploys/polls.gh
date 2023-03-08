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


def nation_report(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE


    regions = Region.objects.all()
    # region_page = request.GET.get('rpage', 1)
    # region_paginator = Paginator(regions, total_per_page)
    # try:
    #     region_data = region_paginator.page(region_page)
    # except PageNotAnInteger:
    #     region_data = region_paginator.page(1)
    # except EmptyPage:
    #     region_data = region_paginator.page(region_paginator.num_pages)
    # context = dict(request=request)
    # region_serializer = RegionSerializer(data, context=context, many=True)
    # if region_data.has_next():
    #     nextPage = data.next_page_number()
    # if region_data.has_previous():
    #     previousPage = data.previous_page_number()
    
    candidate_qs = Candidate.objects.all() \
                            .prefetch_related(
                                Prefetch(
                                    'results',
                                    queryset=Result.objects.all(),
                                    to_attr="position_candidate_results"
                                )
                            )
    '''
    print("::::::::::::::::::::::::::::")
    for region in regions:
        region_lookup = region.title.lower().replace(' ', '_')
        region_lookup = f'result_{region_lookup}'
        # print(region_lookup)
        candidate_qs = candidate_qs \
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
    for candidate in candidate_qs.all():
        print('::::::::::::::::::::::::::::::::::::::::::::::::::')
        print('full_name', candidate.full_name)
        print('party', candidate.party.title)
        print('result_ashanti', candidate.result_ashanti)
        print('result_ahafo', candidate.result_ahafo)
        print('result_bono', candidate.result_bono)
        print('result_bono_east', candidate.result_bono_east)
        print('result_central', candidate.result_central)
        print('result_eastern', candidate.result_eastern)
        print('result_greater_accra', candidate.result_greater_accra)
        print('result_north_east', candidate.result_north_east)
        print('result_northern', candidate.result_northern)
        print('result_oti', candidate.result_oti)
        print('result_upper_east', candidate.result_upper_east)
        print('result_upper_west', candidate.result_upper_west)
        print('result_savannah', candidate.result_savannah)
        print('result_volta', candidate.result_volta)
        print('result_western', candidate.result_western)
        print('result_western_north', candidate.result_western_north)
    '''

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
                                            queryset=Result.objects.all(),
                                            to_attr="results_total"
                                        )
                                    )
        for region in regions:
            region_lookup = region.title.lower().replace(' ', '_')
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
        print(candidate,
                candidate.results,
                candidate.party.title,
                candidate.results_ashanti,
                candidate.results_ahafo,
                candidate.results_bono,
                candidate.results_bono_east,
                candidate.results_central,
                candidate.results_eastern,
                candidate.results_greater_accra,
                candidate.results_north_east,
                candidate.results_northern,
                candidate.results_oti,
                candidate.results_upper_east,
                candidate.results_upper_west,
                candidate.results_savannah,
                candidate.results_volta,
                candidate.results_western,
                candidate.results_western_north,
              )
        '''


    parties = Party.objects.all()
    # party_page = request.GET.get('ppage', 1)
    # party_paginator = Paginator(party, total_per_page)
    # try:
    #     party_data = party_paginator.page(party_page)
    # except PageNotAnInteger:
    #     party_data = party_paginator.page(1)
    # except EmptyPage:
    #     party_data = party_paginator.page(party_paginator.num_pages)
    # context = {'request': request}
    # party_serializer = PartySerializer(party_data, context=context, many=True)
    # if party_data.has_next():
    #     party_next_page = party_data.next_page_number()
    # if party_data.has_previous():
    #     party_previous_age = party_data.previous_page_number()


    context = {
        'title': 'National Collation Results',
        'regions': regions, # region_serializer.data,
        'parties': parties, # party_serializer.data,
        'candidates': candidate_lists,
        # 'count': paginator.count,
        # 'numpages' : paginator.num_pages,
        # 'columns': [{'title': 'title'}, {'title': 'office_title'}],
        'next_link': '/poll/offices/?page=' + str(nextPage),
        'prev_link': '/poll/offices/?page=' + str(previousPage)
    }
    return render(request, "report/nation_report.html", context)

'''
def office_detail(request, pk=None):
    data = get_object_or_404(Office, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = OfficeForm(initial=initial)
    else:
        form = OfficeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            office = form.cleaned_data['office']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                office = Office(code=code, title=title, office=office)
                office.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "poll/office_form.html", {"form": form})


def success_view(request):
    form = OfficeForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "poll/office_form.html", context)
'''


