
from django.conf.urls import url
from options import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^graphdata$', views.GraphData.as_view(), name='graphdata'),
	url(r'^stgyform$', views.NewStrategy.as_view(), name='stgyform'),
	url(r'^legsform$', views.AddLeg.as_view(), name='legsform'),
	url(r'^displaylegs$', views.DisplayLegs.as_view(), name='displaylegs'),
	url(r'^deleteleg$', views.DeleteLeg.as_view(), name='deleteleg'),
	url(r'^strategyinfo$', views.StrategyInfo.as_view(), name='strategyinfo'),
	url(r'^clear$', views.ClearData.as_view(), name='clear'),
	url(r'^strategydata$', views.StrategyData.as_view(), name='strategydata'),
	url(r'^convert$', views.ChooseModel.as_view(), name='convert'),

]
