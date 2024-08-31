from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('user/list', UserListAPIView.as_view(), name='user-list'),
    path('user/create', UserCreateAPIView.as_view(), name='user-create'),
    path('user/retrieve-qr', UserRetrieveAPIView.as_view(), name='user-qr'),
    path('user/search', UserRetrieveDNIView.as_view(), name='user-dni'),
    path('user/confirm/<int:user_id>', UserUpdatePaymentView.as_view(), name='user-confirm'),
    path('user/payment/<int:zone_id>', UserGetImageByZoneView.as_view(), name='zone-image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)