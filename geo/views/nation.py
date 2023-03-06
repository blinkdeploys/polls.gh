from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geo.models import Nation
from geo.serializers import NationSerializer

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from geo.forms import NationForm
from poll.constants import ROWS_PER_PAGE


def nation_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    nation = Nation.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(nation, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = NationSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Nations',
        'data': serializer.data,
        'count': paginator.count,
        'columns': [{'title': 'code'}, {'title': 'title'}],
        'numpages' : paginator.num_pages,
        'next_link': '/geo/nations/?page=' + str(nextPage),
        'prev_link': '/geo/nations/?page=' + str(previousPage)
    }
    return render(request, "geo/nation_list.html", context)


def nation_detail(request, pk=None):
    data = get_object_or_404(Nation, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
    }
    if request.method == "GET":
        form = NationForm(initial=initial)
    else:
        form = NationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            agent = form.cleaned_data['agent']
            try:
                nation = Nation(code=code, title=title, agent=agent)
                nation.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "geo/nation_form.html", {"form": form})


def success_view(request):
    form = NationForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "geo/nation_form.html", context)


