from django.conf.urls import patterns, include, url
from .views import ResultClassDetail, ResultDetail, ResultClassList, ResultClassSearch

urlpatterns = patterns('',
    url(r'result-class/$',                          ResultClassList.as_view(),   name='result-class-list'),
    url(r'result-class/(?P<slug>[-_\w]+)/$',        ResultClassDetail.as_view(), name='result-class-detail'),
    url(r'result-class/(?P<slug>[-_\w]+)/search/$', ResultClassSearch.as_view(), name='result-class-search'),
    url(r'result/(?P<pk>\d+)/$',                    ResultDetail.as_view(),      name='result-detail'),
)
