from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geo.models import Nation
from geo.serializers import NationSerializer
from poll.constants import ROWS_PER_PAGE


@api_view(['GET', 'POST'])
def nation_list(request):
    """
    List nation or create a new nation
    """
    if request.method == "GET":
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
        
        return Response({
            'data': serializer.data,
            'count': paginator.count,
            'numpages' : paginator.num_pages,
            'next_link': '/nations/?page=' + str(nextPage),
            'prev_link': '/nations/?page=' + str(previousPage)
        })
    elif request.method == 'POST':
        serializer = NationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
def nation_detail(request, pk):
    """
    Retrieve, update or delete a custumer by id/pk
    """

    try:
        nation = Nation.objects.get(pk=pk)
    except Nation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NationSerializer(nation, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NationSerializer(nation, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        nation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
