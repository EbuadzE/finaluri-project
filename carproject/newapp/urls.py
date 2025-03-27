from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import CarsView,MyCarsDetailView,AboutUs
app_name = 'cars'

urlpatterns = [
    path('', CarsView.as_view(), name='index'),
    path('detail/<int:pk>/', MyCarsDetailView.as_view(), name = 'detail_car' ),
    path('about/', AboutUs.as_view(), name='about')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
