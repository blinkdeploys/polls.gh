import json
import redis
import django_rq
from django.urls import reverse
from django.conf import settings
from rq.job import Job, JobStatus, cancel_job, get_current_job
from rest_framework.decorators import api_view
from rest_framework.response import Response
from report.tasks import collation_task, clear_collation_task
from django.shortcuts import render, redirect


# Connect to our Redis instance
REDIS_INSTANCE = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   db=settings.REDIS_DB)



def extract_all_values():
    keys = REDIS_INSTANCE.scan_iter('*')
    vals = []
    for key in keys:
        typeof = REDIS_INSTANCE.type(key)
        if typeof == "string":
            vals = [REDIS_INSTANCE.get(key)]
        if typeof == "hash":
            vals = REDIS_INSTANCE.hgetall(key)
        if typeof == "zset":
            vals = REDIS_INSTANCE.zrange(key, 0, -1)
        if typeof == "list":
            vals = REDIS_INSTANCE.lrange(key, 0, -1)
        if typeof == "set":
            vals = REDIS_INSTANCE.smembers(key)
    return vals


def extract_redis_value(REDIS_INSTANCE, redis_key):
    '''Extract the correct type of data based on the data type'''
    # https://stackoverflow.com/questions/37953019/wrongtype-operation-against-a-key-holding-the-wrong-kind-of-value-php
    redis_value = None
 
    # if not REDIS_INSTANCE:
    typeof = REDIS_INSTANCE.type(redis_key) # type(key)
    if typeof in [b'bytes', b'stream']:
        # redis_value = REDIS_INSTANCE.xread(redis_key.decode("utf-8"))
        pass
    elif typeof == b'string':
        redis_value = REDIS_INSTANCE.get(redis_key.decode("utf-8"))
    elif typeof == b'hash':
        redis_value = REDIS_INSTANCE.hgetall(redis_key.decode("utf-8")) # HGET or HMGET or HGETALL
    elif typeof == b'set':
        redis_value = REDIS_INSTANCE.smembers(redis_key.decode("utf-8"))
    elif typeof == b'zset':
        redis_value = REDIS_INSTANCE.zrange(redis_key.decode("utf-8"), 0, -1)
    elif typeof == b'list':
        redis_value = REDIS_INSTANCE.lrange(redis_key.decode("utf-8"), 0, -1)
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


@api_view(['GET'])
def dequeue_collation(request, jid=None):
    # job_id = job # request.GET.get('job_id')
    redis_conn = django_rq.get_connection()
    job_id=jid.split(':')[2] 

    job = None
    try:
        job = Job.fetch(job_id, redis_conn) # fetch Job from redis
    except Exception as e: # NoSuchJobError
        # logger.info(job_id)
        print(e)

    if job is not None:
        if job.is_finished:
            # message=job.return_value
            response = dict(state='Job completed',
                            job_key=jid,
                            code=201,)
        elif job.is_queued:
            response = dict(status='Job currently in queue',
                            job_key=jid,
                            code=102,)
        elif job.is_started:
            response = dict(status='Job still waiting',
                            job_key=jid,
                            code=100,)
        elif job.is_failed:
            response = dict(status='Job has failed',
                            code=500,
                            job_key=jid,)
    else:
        response = dict(status='Job not found',
                        code=404,
                        job_key=jid,)
    return Response(response, 201)


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in REDIS_INSTANCE.keys("*"):
            key_value = key.decode("utf-8")
            redis_value = extract_redis_value(REDIS_INSTANCE, key)
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
        REDIS_INSTANCE.set(key, value)
        response = dict(
            msg=f"{key} successfully set to {value}"
        )
        return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = extract_redis_value(REDIS_INSTANCE, kwargs['key'])
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
            value = extract_redis_value(REDIS_INSTANCE, kwargs['key'])
            if value:
                REDIS_INSTANCE.set(kwargs['key'], new_value)
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
            result = REDIS_INSTANCE.delete(kwargs['key'])
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
