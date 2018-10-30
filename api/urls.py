from django.conf.urls import url

from api.views import (GoodView, NewUser, GetToken, OrderView, CartView)

urlpatterns = [
    url(r'^new_user/$', NewUser.as_view(), name='register_new_user'),
    url(r'^get_token/$', GetToken.as_view(), name='get_token'),
    url(r'^items/$', GoodView.as_view({'get': 'list'})),
    url(r'^items/(?P<pk>[a-z0-9]+)/?$', GoodView.as_view({'get': 'retrieve'})),
    url(r'^order/$', OrderView.as_view({'get': 'retrieve'})),
    url(r'^orders/$', OrderView.as_view({'get': 'list'})),
    url(r'^orders/(?P<pk>[a-z0-9]+)/?$', OrderView.as_view({'get': 'retrieve'})),
    url(r'^cart/$', CartView.as_view({'post': 'post'})),
    url(r'^cart/(?P<pk>[a-z0-9]+)/?$', CartView.as_view({'delete': 'delete'})),

]
