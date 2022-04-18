from django.urls import path, re_path
from django.conf.urls.static import static
from .views import *
from django.conf import settings

app_name = 'operators'
urlpatterns = [
    path('', main, name='main'),
    path('apps_list/', AppListView.as_view(), name='apps_list'),
    path('del_app/', del_app, name='del_app'),
    path('app_detail/<int:pk>', AppDetailView.as_view(), name='app_detail'),
    path('experts_list/', ExpertsListView.as_view(), name='experts_list'),
    path('edit_exp/', edit_exp, name='edit_exp'),
    path('new_exp/', new_exp, name='new_exp'),
    path('import_exp/', import_exp, name='import_exp'),
    path('del_exp/', del_exp, name='del_exp'),
    path('periods_list/', PeriodsListView.as_view(), name='periods_list'),
    path('period_edit/', period_edit, name='period_edit'),
    path('period_new/', period_new, name='period_new'),
    path('period_del/', period_del, name='period_del'),
    path('expertise_main/', expertise_main, name='expertise_main'),
    path('new_distribution/', new_distribution, name='new_distribution'),
    path('del_distrib/', del_distrib, name='del_distrib'),
    path('distribution_list/', DistributionListView.as_view(), name='distribution_list'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)