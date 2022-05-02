
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('classes', views.classes_view, name = 'classes_view'),
    path('addclass', views.add_class, name = 'add_class'),
    path('classes/submit', views.submit, name='submit'),
    path('removeclass', views.remove_class, name = 'remove_class'),
    path('classes/remove', views.remove, name='remove'),
    path('toggleclass', views.toggle_class, name='toggle_class'),
    path('classes/toggle', views.toggle, name='toggle'),
    path('untoggleclass', views.untoggle_class, name="untoggle_class"),
    path('classes/untoggle', views.untoggle, name='untoggle'),
    re_path(r'rooms/$', views.all_rooms, name="all_rooms"),
    re_path(r'rooms/token$', views.token, name="token"),
    re_path(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    path('maps', views.AddLocationView.as_view(), name = 'maps'),
    path('maps/update/<int:pk>', views.UpdateLocationView.as_view(), name = 'update'),
    #path('maps/delete/<int:id>', views.DeleteUserFromLocation, name = 'delete'),
    path('info_input', views.input_information, name='info'),
    path('info_input/submit', views.info_submit, name='info_submit'),
    path('matching', views.match, name='matching'),
    path('clear_matches', views.clearmatches, name = 'clear')
]
