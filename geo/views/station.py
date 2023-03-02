from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from geo.models import Station
from geo.serializers import StationSerializer
from geo.forms import StationForm
from poll.constants import ROWS_PER_PAGE


def station_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    station = Station.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(station, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = StationSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Stations',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': ['code', 'title', 'constituency.title'],
        'next_link': '/geo/stations/?page=' + str(nextPage),
        'prev_link': '/geo/stations/?page=' + str(previousPage)
    }
    return render(request, "geo/station_list.html", context)


"""
def station_detail(request, pk):
    Retrieve, update or delete a custumer by id/pk

    try:
        station = Station.objects.get(pk=pk)
    except Station.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StationSerializer(station, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StationSerializer(station, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


def station_detail(request, pk=None):
    data = get_object_or_404(Station, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'details': data.details,
        'constituency': data.constituency,
        'agent': data.agent,
        'status': data.status,
    }
    if request.method == "GET":
        form = StationForm(initial=initial)
    else:
        form = StationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            agent = form.cleaned_data['agent']
            try:
                station = Station(code=code, title=title, agent=agent)
                station.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "geo/station_form.html", {"form": form})


def success_view(request):
    form = StationForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "geo/station_form.html", context)


