from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from people.models import Party
from people.serializers import PartySerializer
from people.forms import PartyForm
from poll.constants import ROWS_PER_PAGE


def party_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    party = Party.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(party, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = PartySerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Parties',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': ['code', 'title', 'total_candidates', 'votes', 'agent'],
        'next_link': '/people/parties/?page=' + str(nextPage),
        'prev_link': '/people/parties/?page=' + str(previousPage)
    }
    return render(request, "people/party_list.html", context)


def party_detail(request, pk=None):
    data = get_object_or_404(Party, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = PartyForm(initial=initial)
    else:
        form = PartyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            party = form.cleaned_data['party']
            try:
                party = Party(code=code, title=title, party=party)
                party.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "people/party_form.html", {"form": form})


def success_view(request):
    form = PartyForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "people/party_form.html", context)


