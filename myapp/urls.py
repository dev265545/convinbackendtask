from django.urls import path
from . import views

urlpatterns = [
    path('rest/v1/calendar/init/', views.GoogleCalendarInitView.as_view(), name='google-calendar-init'),
    path('rest/v1/calendar/', views.MyView.as_view(), name='myview'),
    path('rest/v1/calendar/redirect/', views.GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
]
