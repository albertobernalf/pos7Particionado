#from django.conf.urls import url
#from django.urls import include, path
from django.urls import re_path


from .viewsFurips import (FuripsList,FuripsDetail,FuripsCreation,    FuripsUpdate,  FuripsDelete)

urlpatterns = [
    re_path(r'^$', FuripsList.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)$', FuripsDetail.as_view(), name='detail'),
    re_path(r'^nuevo$', FuripsCreation.as_view(), name='new'),
    re_path(r'^editar/(?P<pk>\d+)$', FuripsUpdate.as_view(), name='edit'),
    re_path(r'^borrar/(?P<pk>\d+)$', FuripsDelete.as_view(), name='delete'),

]
