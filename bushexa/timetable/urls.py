from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

appname = 'timetable'
urlpatterns = [
    path('', views.index, name='index'),
    # path('departure/', cache_page(1 * 60)(views.TimeBasedBusListView.as_view()), name='departure'),
    path('departure/', cache_page(10)(views.TimeBasedBusListView.as_view()), name='departure'),
    path('busno/', views.BusNumberBasedBusListView.as_view(), name='busno'),
]
