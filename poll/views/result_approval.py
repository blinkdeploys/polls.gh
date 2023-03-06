from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from poll.models import ResultApproval
from poll.serializers import ResultApprovalSerializer
from poll.forms import ResultApprovalForm
from poll.constants import ROWS_PER_PAGE


def result_approval_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    result_approval = ResultApproval.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(result_approval, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = ResultApprovalSerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Result Approvals',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': [{'title': 'result'}, {'title': 'approved_at'}, {'title': 'approving_agent.name'}, {'title': 'result.title'}],
        'next_link': '/poll/result_approvals/?page=' + str(nextPage),
        'prev_link': '/poll/result_approvals/?page=' + str(previousPage)
    }
    return render(request, "poll/result_approval_list.html", context)


def result_approval_detail(request, pk=None):
    data = get_object_or_404(ResultApproval, pk=pk)
    initial = {
        'pk': data.pk,
        'code': data.code,
        'title': data.title,
        'status': data.status,
    }
    if request.method == "GET":
        form = ResultApprovalForm(initial=initial)
    else:
        form = ResultApprovalForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            result_approval = form.cleaned_data['result_approval']
            try:
                # send_mail(subject, message, from_email, ["admin@example.com"])
                result_approval = ResultApproval(code=code, title=title, result_approval=result_approval)
                result_approval.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "poll/result_approval_form.html", {"form": form})


def success_view(request):
    form = ResultApprovalForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "poll/result_approval_form.html", context)


