from django.conf.urls import url
from schools import views


urlpatterns = [
    url(r'^canon/', views.web, name='index_public'),
]
