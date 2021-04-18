from django.conf.urls import url
from django.urls import path, include
urlpatterns = [
    url('', include('api.urls'))
    ]