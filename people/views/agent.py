from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from people.models import Agent
from people.serializers import AgentSerializer
from people.forms import AgentForm
from poll.constants import ROWS_PER_PAGE


def agent_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    agent = Agent.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(agent, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = AgentSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Agents',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': ['first_name', 'last_name', 'email', 'phone', 'status'],
        'next_link': '/people/agents/?page=' + str(nextPage),
        'prev_link': '/people/agents/?page=' + str(previousPage)
    }
    return render(request, "people/agent_list.html", context)


def agent_detail(request, pk=None):
    data = get_object_or_404(Agent, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = AgentForm(initial=initial)
    else:
        form = AgentForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            agent = form.cleaned_data['agent']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                agent = Agent(code=code, title=title, agent=agent)
                agent.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "people/agent_form.html", {"form": form})


def success_view(request):
    form = AgentForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "people/agent_form.html", context)


