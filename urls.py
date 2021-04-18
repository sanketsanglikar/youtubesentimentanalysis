from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.send_file)
    # path('sentiment', ),
    # path('wordcloud', )
]