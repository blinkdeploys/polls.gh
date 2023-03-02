from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geo.models import Constituency
from geo.serializers import ConstituencySerializer
from poll.constants import ROWS_PER_PAGE


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
            'next_link': '/constituencies/?page=' + str(nextPage),
            'prev_link': '/constituencies/?page=' + str(previousPage)
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
