from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from poll.models import Result
from people.models import Party
from poll.serializers import ResultSerializer
from poll.forms import ResultForm
from poll.constants import ROWS_PER_PAGE


def result_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    
    result = Result.objects.all()
    party = Party.objects.all()

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
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': ['candidate_details', 'station.title', 'total_votes', 'constituency_agent', 'result_sheet'],
        'next_link': '/poll/results/?page=' + str(nextPage),
        'prev_link': '/poll/results/?page=' + str(previousPage)
    }
    return render(request, "poll/result_list.html", context)


def result_detail(request, pk=None):
    data = get_object_or_404(Result, pk=pk)
    initial = {
        'pk': data.pk,
        'constituency_agent': data.constituency_agent,
        'candidate': data.candidate,
        'station': data.station,
        'total_votes': data.total_votes,
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


