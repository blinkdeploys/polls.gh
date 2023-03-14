import json
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from time import sleep
from faker import Faker
import django_rq
from ..tasks import collation_task, clear_collation_task
from rq.job import Job, JobStatus, cancel_job, get_current_job
import redis
# from django_q.tasks import async_task
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   db=settings.REDIS_DB)



def extract_all_values():
    keys = redis_instance.scan_iter('*')
    vals = []
    for key in keys:
        typeof = redis_instance.type(key)
        if typeof == "string":
            vals = [redis_instance.get(key)]
        if typeof == "hash":
            vals = redis_instance.hgetall(key)
        if typeof == "zset":
            vals = redis_instance.zrange(key, 0, -1)
        if typeof == "list":
            vals = redis_instance.lrange(key, 0, -1)
        if typeof == "set":
            vals = redis_instance.smembers(key)
    return vals


def extract_redis_value(redis_instance, redis_key):
    '''Extract the correct type of data based on the data type'''
    # https://stackoverflow.com/questions/37953019/wrongtype-operation-against-a-key-holding-the-wrong-kind-of-value-php
    redis_value = None
 
    # if not redis_instance:
    typeof = redis_instance.type(redis_key) # type(key)
    if typeof in [b'bytes', b'stream']:
        # redis_value = redis_instance.xread(redis_key.decode("utf-8"))
        pass
    elif typeof == b'string':
        redis_value = redis_instance.get(redis_key.decode("utf-8"))
    elif typeof == b'hash':
        redis_value = redis_instance.hgetall(redis_key.decode("utf-8")) # HGET or HMGET or HGETALL
    elif typeof == b'set':
        redis_value = redis_instance.smembers(redis_key.decode("utf-8"))
    elif typeof == b'zset':
        redis_value = redis_instance.zrange(redis_key.decode("utf-8"), 0, -1)
    elif typeof == b'list':
        redis_value = redis_instance.lrange(redis_key.decode("utf-8"), 0, -1)
    # print('::::::::::::::::::::::::::::::')
    # print(redis_key, typeof, redis_key.decode("utf-8"), redis_value)
    return redis_value



@api_view(['GET'])
def clear_collation(request):
    queue = django_rq.get_queue('default')
    job = queue.enqueue(clear_collation_task)
    job_key = job.key.decode("utf-8")
    response = dict(
        status=201,
        message='Currently processing.',
        job=job_key,
    )
    return redirect(reverse('dequeue', kwargs=dict(jid=job_key)), response, 201)


@api_view(['GET'])
def enqueue_collation(request):
    queue = django_rq.get_queue('default')
    context = dict(
        message='Sending messages via context...',
    )
    job = queue.enqueue(collation_task, context=context)
    job_key = job.key.decode("utf-8")
    response = dict(
        status=201,
        message='Currently processing.',
        job=job_key,
    )
    return redirect(reverse('dequeue', kwargs=dict(jid=job_key)), response, 201)
    # return Response(response, 201)
    # return HttpResponse(response, content_type='application/json')


@api_view(['GET'])
def dequeue_collation(request, jid=None):
    # job_id = job # request.GET.get('job_id')
    redis_conn = django_rq.get_connection()
    job_id=jid.split(':')[2] 

    job = None
    try:
        # logger.info(job_id)
        job = Job.fetch(job_id, redis_conn) # fetch Job from redis
    except Exception as e: # NoSuchJobError
        print(e)

    if job is not None:
        if job.is_finished:
            response = dict(state='Job completed',
                            job_key=jid,
                            code=201,
                            # message=job.return_value
                            )
        elif job.is_queued:
            response = dict(status='Job currently in queue',
                            job_key=jid,
                            code=102,
                            )
        elif job.is_started:
            response = dict(status='Job still waiting',
                            job_key=jid,
                            code=100,
                            )
        elif job.is_failed:
            response = dict(status='Job has failed',
                            code=500,
                            job_key=jid,
                            )
    else:
        response = dict(status='Job not found',
                        code=404,
                        job_key=jid,
                        )
    return Response(response, 201)
    # return HttpResponse(json.dumps(ret), content_type="application/json")


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            key_value = key.decode("utf-8")
            redis_value = extract_redis_value(redis_instance, key)
            # print(key, type(key), type(key_value))
            # if redis_value is not None and type(key) == str: # in [str, int, float, bool]:
            if redis_value is not None \
                and ':' not in key_value:
                items[key_value] = redis_value
                count += 1
        response = dict(
            count=count,
            msg=f"Found {count} items.",
            items=items
        )
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = dict(
            msg=f"{key} successfully set to {value}"
        )
        return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = extract_redis_value(redis_instance, kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = dict(
                    key=kwargs['key'],
                    value=None,
                    msg='Not found'
                )
                return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = extract_redis_value(redis_instance, kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = dict(
                    key=kwargs['key'],
                    value=value,
                    msg=f"Successfully updated {kwargs['key']}"
                )
                return Response(response, status=200)
            else:
                response = dict(
                    key=kwargs['key'],
                    value=None,
                    msg='Not found'
                )
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = dict(
                    msg=f"{kwargs['key']} successfully deleted"
                )
                return Response(response, status=404)
            else:
                response = dict(
                    key=kwargs['key'],
                    value=None,
                    msg='Not found'
                )
                return Response(response, status=404)
