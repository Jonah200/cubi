from django.urls import include, path

import django_eventstream

from .views import (
    AssociateDeviceView,
    CsrfView,
    LoginView,
    LogoutView,
    MeView,
    SignupView,
    SolvesView,
    StatsView,
)

urlpatterns = [
    path('auth/csrf/', CsrfView.as_view(), name='csrf'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('devices/associate/', AssociateDeviceView.as_view(), name='associate-device'),
    path('solves/', SolvesView.as_view(), name='solves'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('events/<channel>/', include(django_eventstream.urls)),
]
