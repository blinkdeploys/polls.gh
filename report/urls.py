# account/urls.py
# from django.urls import path
from django.conf.urls import url
from report import views as report_views


urlpatterns = [

    url(r'^presidential/nation/$', report_views.nation_report, name="nation_report"),
    url(r'^presidential/region/(?P<rpk>[0-9]+)$', report_views.region_report, name="region_report"),
    url(r'^presidential/constituency/(?P<cpk>[0-9]+)$', report_views.constituency_report, name="constituency_report"),

    url(r'^parliamentary/nation/$', report_views.nation_parliamentary_report, name="nation_parliamentary_report"),
    url(r'^parliamentary/region/(?P<rpk>[0-9]+)$', report_views.region_parliamentary_report, name="region_parliamentary_report"),
    url(r'^parliamentary/constituency/(?P<cpk>[0-9]+)$', report_views.constituency_parliamentary_report, name="constituency_parliamentary_report"),
    url(r'^parliamentary/station/(?P<spk>[0-9]+)$', report_views.station_parliamentary_report, name="station_parliamentary_report"),

    # url(r'^event/(?P<pk>[0-9]+)$', report_views.event_detail, name="event_detail"),
]
