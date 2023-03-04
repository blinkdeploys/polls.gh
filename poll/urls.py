# account/urls.py
# from django.urls import path
from django.conf.urls import url
from poll import views as poll_views
# from .views import RegisterView


urlpatterns = [
    # path("register/", RegisterView.as_view(), name="register"),

    url(r'^events/$', poll_views.event_list, name="event_list"),
    url(r'^event/$', poll_views.event_detail, name="event_detail"),
    url(r'^event/(?P<pk>[0-9]+)$', poll_views.event_detail, name="event_detail"),
    url(r'^offices/$', poll_views.office_list, name="office_list"),
    url(r'^office/$', poll_views.office_detail, name="office_detail"),
    url(r'^office/(?P<pk>[0-9]+)$', poll_views.office_detail, name="office_detail"),
    url(r'^positions/$', poll_views.position_list, name="position_list"),
    url(r'^position/$', poll_views.position_detail, name="position_detail"),
    url(r'^position/(?P<pk>[0-9]+)$', poll_views.position_detail, name="position_detail"),

    url(r'^result/$', poll_views.result_detail, name="result_detail"),
    url(r'^result/(?P<pk>[0-9]+)$', poll_views.result_detail, name="result_detail"),
    url(r'^results/$', poll_views.result_list, name="result_list"),
    url(r'^result/stations/$', poll_views.station_list, name="result_station_list"),
    url(r'^result/station/(?P<spk>[0-9]+)$', poll_views.position_list, name="result_position_list"),
    url(r'^result/station/(?P<spk>[0-9]+)/position/(?P<ppk>[0-9]+)$', poll_views.candidate_list, name="result_candidate_list"),

    url(r'^result_approvals/$', poll_views.result_approval_list, name="result_approval_list"),
    url(r'^result_approval/$', poll_views.result_approval_detail, name="result_approval_detail"),
    url(r'^result_approval/(?P<pk>[0-9]+)$', poll_views.result_approval_detail, name="result_approval_detail"),

]
