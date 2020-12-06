from django.urls import path
from . import views
#urlpatterns = [path('', views.index, name='index'),]
from .views import PredView


urlpatterns = [
    path('', PredView.as_view(), name='index'),
]