from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('user/list', UserListAPIView.as_view(), name='user-list'),
    path('user/create', UserCreateAPIView.as_view(), name='user-create'),
    path('user/retrieve-qr', UserRetrieveAPIView.as_view(), name='user-qr'),
    path('user/search', UserRetrieveDNIView.as_view(), name='user-dni'),
    path('user/search-id', UserRetrieveIDView.as_view(), name='user-id'),
    path('user/asistence', UserAsistenceView.as_view(), name='asistence'),
    path('user/confirm/<int:us_id>', UserUpdatePaymentView.as_view(), name='user-confirm'),
    path('user/payment/<int:zone_id>', UserGetImageByZoneView.as_view(), name='zone-image'),
    
    path('report/days', AsistenciaPorZonaView.as_view(), name='report-days'),
    path('report/asistence-days', AsistenciaPorDiaLugarView.as_view(), name='asistence-days'),
    path('report/asistence-total', AsistenciaTotalView.as_view(), name='asistence-total'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)