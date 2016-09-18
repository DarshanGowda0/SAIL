from django.conf.urls import url
from suggest_faq import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^add_user/$', views.AddUser.as_view()),
    url(r'^ManageTables/$', views.ManageTables.as_view()),
    url(r'^train/$', views.Train.as_view()),
    url(r'^predict/$', views.Predict.as_view()),
]
