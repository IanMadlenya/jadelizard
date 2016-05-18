
from django.conf.urls import url
from options import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^graphdata$', views.GraphData.as_view(), name='graphdata'),
	url(r'^stgyform$', views.NewStrategy.as_view(), name='stgyform'),
	url(r'^updatestgy$', views.UpdateStrategy.as_view(), name='updatestgy'),
	url(r'^legsform$', views.AddLeg.as_view(), name='legsform'),
	url(r'^displaylegs$', views.DisplayLegs.as_view(), name='displaylegs'),
	url(r'^getleg$', views.GetLeg.as_view(), name='getleg'),
	url(r'^deleteleg$', views.DeleteLeg.as_view(), name='deleteleg'),
	url(r'^updateleg$', views.UpdateLeg.as_view(), name='updateleg'),
	url(r'^strategyinfo$', views.StrategyInfo.as_view(), name='strategyinfo'),
	url(r'^clear$', views.ClearData.as_view(), name='clear'),
	url(r'^strategydata$', views.StrategyData.as_view(), name='strategydata'),
	url(r'^choosemodel$', views.ChooseModel.as_view(), name='choosemodel'),
	url(r'^volcalc$', views.TrailingVol.as_view(), name='volcalc'),
	url(r'^getr$', views.GetR.as_view(), name='getr'),
	url(r'^loadtemplate$', views.StrategyTemplate.as_view(), name='loadtemplate'),
]
