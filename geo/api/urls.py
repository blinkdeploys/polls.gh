# account/urls.py
# from django.urls import path
from django.conf.urls import url
from .views import nation, region, constituency, station


urlpatterns = [
    url(r'^nations/$', nation.nation_list),
    url(r'^nation/(?P<pk>[0-9]+)$', nation.nation_detail),
    url(r'^regions/$', region.region_list),
    url(r'^region/(?P<pk>[0-9]+)$', region.region_detail),
    url(r'^constituencies/$', constituency.constituency_list),
    url(r'^constituency/(?P<pk>[0-9]+)$', constituency.constituency_detail),
    url(r'^stations/$', station.station_list),
    url(r'^station/(?P<pk>[0-9]+)$', station.station_detail),
]
