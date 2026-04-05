from django.urls import path

from .views import AssociateDeviceView

urlpatterns = [
    path('devices/associate/', AssociateDeviceView.as_view(), name='associate-device'),
]
