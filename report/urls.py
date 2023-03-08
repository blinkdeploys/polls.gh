# account/urls.py
# from django.urls import path
from django.conf.urls import url
from report import views as report_views


urlpatterns = [
    url(r'^nation/$', report_views.nation_report, name="nation_report"),
    url(r'^region/(?P<rpk>[0-9]+)$', report_views.region_report, name="region_report"),
    url(r'^constituency/(?P<cpk>[0-9]+)$', report_views.constituency_report, name="constituency_report"),
    # url(r'^station/$', report_views.station_report, name="station_report"),

    # url(r'^event/(?P<pk>[0-9]+)$', report_views.event_detail, name="event_detail"),
]
