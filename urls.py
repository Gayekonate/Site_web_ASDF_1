

from django.urls import path
from membres.views import index, add_membre

urlpatterns = [
    path('', index, name="index"),
    path('add', add_membre, name="add-membre"),

]
