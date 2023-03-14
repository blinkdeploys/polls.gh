from django.conf.urls import url
from report import views as report_views
from report.api import views as api_views


urlpatterns = [
    url(r'^clear/$', api_views.clear_collation, name="clear-results"),
    url(r'^enqueue/$', api_views.enqueue_collation, name="enqueue"),
    url(r'^dequeue/(?P<jid>rq:job:[0-9a-zA-Z]+-[0-9a-zA-Z]+-[0-9a-zA-Z]+-[0-9a-zA-Z]+-[0-9a-zA-Z]+)$', api_views.dequeue_collation, name="dequeue"),

    url(r'^collate/items$', api_views.manage_items, name="items"),
    url(r'^collate/items/<slug:key>$', api_views.manage_item, name="single_item"),

    url(r'^presidential/nation/$', report_views.nation_report, name="nation_report"),
    url(r'^presidential/region/(?P<rpk>[0-9]+)$', report_views.region_report, name="region_report"),
    url(r'^presidential/constituency/(?P<cpk>[0-9]+)$', report_views.constituency_report, name="constituency_report"),

    url(r'^parliamentary/nation/$', report_views.nation_parliamentary_report, name="nation_parliamentary_report"),
    url(r'^parliamentary/region/(?P<rpk>[0-9]+)$', report_views.region_parliamentary_report, name="region_parliamentary_report"),
    url(r'^parliamentary/constituency/(?P<cpk>[0-9]+)$', report_views.constituency_parliamentary_report, name="constituency_parliamentary_report"),
    url(r'^parliamentary/station/(?P<spk>[0-9]+)$', report_views.station_parliamentary_report, name="station_parliamentary_report"),
]
