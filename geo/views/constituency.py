import json
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geo.models import Constituency

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from geo.serializers import ConstituencySerializer
from geo.forms import ConstituencyForm
from poll.constants import ROWS_PER_PAGE


def constituency_list(request):
    data = []
    nextPage = 1
    previousPage = 1
    total_per_page = ROWS_PER_PAGE
    constituency = Constituency.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(constituency, total_per_page)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = ConstituencySerializer(data, context={'request': request}, many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    context = {
        'title': 'Constituencies',
        'data': serializer.data,
        'count': paginator.count,
        'numpages' : paginator.num_pages,
        'columns': ['title', 'region.title'],
        'next_link': '/geo/constituencies/?page=' + str(nextPage),
        'prev_link': '/geo/constituencies/?page=' + str(previousPage)
    }
    return render(request, "geo/constituency_list.html", context)


def constituency_detail(request, pk=None):
    data = get_object_or_404(Constituency, pk=pk)
    initial = {
        'pk': data.pk,
        'title': data.title,
        'region': data.region,
        'agent': data.agent,
        'details': data.details,
        'status': data.status,
    }
    if request.method == "GET":
        form = ConstituencyForm(initial=initial)
    else:
        form = ConstituencyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            title = form.cleaned_data["title"]
            agent = form.cleaned_data['agent']
            try:
                constituency = Constituency(code=code, title=title, agent=agent)
                constituency.save()
            except BadHeaderError:
                return HttpResponse("Error saving record.")
            return redirect("Record successfully saved")
    return render(request, "geo/constituency_form.html", {"form": form})


def success_view(request):
    form = ConstituencyForm()
    context = {"form": form, "message": "Success! Thank you for your message."}
    return render(request, "geo/constituency_form.html", context)


'''
@api_view(['GET', 'POST'])
def constituency_list(request):
    """
    List constituency or create a new constituency
    """
    if request.method == "GET":
        data = []
        nextPage = 1
        previousPage = 1
        total_per_page = ROWS_PER_PAGE
        constituency = Constituency.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(constituency, total_per_page)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ConstituencySerializer(data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()
        
        return Response({
            'data': serializer.data,
            'count': paginator.count,
            'numpages' : paginator.num_pages,
            'next_link': '/geo/constituencies/?page=' + str(nextPage),
            'prev_link': '/geo/constituencies/?page=' + str(previousPage)
        })
    elif request.method == 'POST':
        serializer = ConstituencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
def constituency_detail(request, pk):
    """
    Retrieve, update or delete a custumer by id/pk
    """

    try:
        constituency = Constituency.objects.get(pk=pk)
    except Constituency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConstituencySerializer(constituency, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ConstituencySerializer(constituency, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        constituency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from django.urls import reverse_lazy
# from django.views import generic
# class RegisterView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/register.html"



'''

