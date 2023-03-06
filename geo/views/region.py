from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geo.models import Region
from geo.serializers import RegionSerializer

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from geo.forms import RegionForm
from poll.constants import ROWS_PER_PAGE


def region_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    region = Region.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(region, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = RegionSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Regions',
        'data': serializer.data,
        'count': paginator.count,
        'columns': [{'title': 'title'}, {'title': 'nation.title'}],
        'numpages' : paginator.num_pages,
        'next_link': '/geo/regions/?page=' + str(nextPage),
        'prev_link': '/geo/regions/?page=' + str(previousPage)
    }
    return render(request, "geo/region_list.html", context)


def region_detail(request, pk=None):
    data = get_object_or_404(Region, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = RegionForm(initial=initial)
    else:
        form = RegionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            agent = form.cleaned_data['agent']
            try:
                region = Region(code=code, title=title, agent=agent)
                region.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "geo/region_form.html", {
        "title": "Region",
        "list_path": "/regions",
        "form": form
    })


def success_view(request):
    form = RegionForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "geo/region_form.html", context)


