
from django.conf.urls import url
from options import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
    url(r'^navbar$', views.NavBar.as_view(), name='navbar'),
]
