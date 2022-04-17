
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('addclass', views.add_class, name = 'add_class'),
    path('classes/submit', views.submit, name='submit'),
    path('removeclass', views.remove_class, name = 'remove_class'),
    path('classes/remove', views.remove, name='remove'),
    path('toggleclass', views.toggle_class, name='toggle_class'),
    path('classes/toggle', views.toggle, name='toggle'),
    path('untoggleclass', views.untoggle_class, name="untoggle_class"),
    path('classes/untoggle', views.untoggle, name='untoggle'),
]