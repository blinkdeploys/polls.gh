from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from people.models import Candidate
from people.serializers import CandidateSerializer
from people.forms import CandidateForm
from poll.constants import ROWS_PER_PAGE


def candidate_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    candidates = Candidate.objects.all()
    # candidate = sorted(Candidate.objects.all(), key=lambda t: t.result_votes, reverse=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(candidates, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    serializer = CandidateSerializer(data, context={'request': request}, many=True)

    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Candidates',
        # 'data': serializer.data,
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': [
            {'title': 'party.code', 'width': 10},
            {'title': 'full_name', 'width': 40},
            {'title': 'position.title', 'width': 40}
        ],
        'column_widths': [5, None, 15],
        'next_link': '/people/candidates/?page=' + str(nextPage),
        'prev_link': '/people/candidates/?page=' + str(previousPage)
    }
    return render(request, "people/candidate_list.html", context)


def candidate_detail(request, pk=None):
    data = get_object_or_404(Candidate, pk=pk)
    initial = {
        'pk': data.pk,
        'prefix': data.prefix,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'other_names': data.other_names,
        'description': data.description,
        'position': data.position,
        'party': data.party,
        'status': data.status,
    }
    if request.method == "GET":
        form = CandidateForm(initial=initial)
    else:
        form = CandidateForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            candidate = form.cleaned_data['candidate']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                candidate = Candidate(code=code, title=title, candidate=candidate)
                candidate.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "people/candidate_form.html", {"form": form})


def success_view(request):
    form = CandidateForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "people/candidate_form.html", context)


