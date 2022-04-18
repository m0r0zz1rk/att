from django.urls import path, re_path
from django.conf.urls.static import static
from .views import *
from django.conf import settings

app_name = 'expert'
urlpatterns = [
    path('', main, name='main'),
    path('expertise/', expertise, name='expertise'),
    path('profile/', profile, name='profile'),
    path('apps/', DistribAppsListView.as_view(), name='apps'),
    path('app_expertise/<int:pk>', DistribAppDetailView.as_view(), name='app_expertise'),
    path('archive/', ArchiveApps.as_view(), name='archive'),
    path('add_mark/', add_mark, name='add_mark'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)