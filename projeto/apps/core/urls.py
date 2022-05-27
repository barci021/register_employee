from django.urls import path
from .views import home, view


urlpatterns = [
    path('', home, name='home'),
    path('view/', view, name='view'),

]