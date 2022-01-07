from typing import Any, Dict
from django.shortcuts import redirect, render
# from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .tools.tools import *
from .tools.helpers import *
from django.utils.cache import add_never_cache_headers

class TimeTableMixin:
    """
    시간 기준으로 버스 목록 표시
    """
    def get_timetable_context(self) -> Dict[str, Any]:
        now = get_now()
        bus_time = get_bustime(now)
        return {
            'request_time': pretty_time(now),
            'time_table': bus_time,
        }

class TimeBasedBusListView(TemplateView, TimeTableMixin):

    template_name = "timetable/departure.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_timetable_context())
        return context

    def dispatch(self, *args, **kwargs):
        response = super(TimeBasedBusListView, self).dispatch(*args, **kwargs)
        response["Cache-Control"] = "no-cache, no-store, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "-1"
        return response


class BusInfoMixin:
    STOP_ID = "196040234"

    """
    버스 번호 기준으로 표시
    """
    def get_businfo_context(self) -> Dict[str, Any]:
        # crawl_arrival() # 추후 API에 직접 요청하는 부분을 삭제할것 **FIXIT**

        bus_info = get_busstop_time(self.STOP_ID)
        stop_name = get_stop_string(self.STOP_ID)
        return {
            'stop_name': stop_name,
            'bus_info': bus_info
        }

class BusNumberBasedBusListView(TemplateView, BusInfoMixin):

    template_name = "timetable/busno.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_businfo_context())
        return context


def index(request):
    return redirect('busno')
