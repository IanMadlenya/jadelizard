
from django.conf.urls import url
from options import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^graphdata$', views.GraphData.as_view(), name='graphdata'),
	url(r'^stgyform$', views.NewStrategy.as_view(), name='stgyform'),
	url(r'^convert$', views.ChooseModel.as_view(), name='convert'),



]
