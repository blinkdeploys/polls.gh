from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from poll.models import Position
from poll.serializers import PositionSerializer
from poll.forms import PositionForm
from poll.constants import ROWS_PER_PAGE


def position_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    position = Position.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(position, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = PositionSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Positions',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': [{'title': 'zone'}, {'title': 'title'}],
        'next_link': '/poll/positions/?page=' + str(nextPage),
        'prev_link': '/poll/positions/?page=' + str(previousPage)
    }
    return render(request, "poll/position_list.html", context)


def position_detail(request, pk=None):
    data = get_object_or_404(Position, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = PositionForm(initial=initial)
    else:
        form = PositionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            position = form.cleaned_data['position']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                position = Position(code=code, title=title, position=position)
                position.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "poll/position_form.html", {"form": form})


def success_view(request):
    form = PositionForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "poll/position_form.html", context)


