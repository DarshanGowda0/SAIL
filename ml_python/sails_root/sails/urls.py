from django.conf.urls import url
from sails import views

urlpatterns = [
#   url(r'threeStepAdd/$', views.threeStepsAdd),
    url(r'trainThisApp/$', views.trainThisApp),
    url(r'predictThisLevel/$', views.predictThisLevel),
]
