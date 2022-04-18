from django.urls import path, re_path
from django.conf.urls.static import static
from .views import *
from django.conf import settings

app_name = 'applications'
urlpatterns = [
    path('', main, name='main'),
    path('profile/', profile, name='profile'),
    path('login/', login_user, name='login_user'),
    path('login_operator/', login_operator, name='login_operator'),
    path('registr/', registr, name='registr'),
    path('logout/', logout_user, name='logout_user'),
    path('apps_choose/', apps_choose, name='apps_choose'),
    path('new_app/', new_app, name='new_app'),
    path('new_app_crits/', new_app_crits, name='new_app_crits'),
    path('new_app_cat', new_app_cat, name='new_app_cat'),
    path('change_crit/', change_crit, name='change_crit'),
    path('upload_crit/', upload_crit, name='upload_crit'),
    path('history_apps/', history_apps, name='history_apps'),
    path('edit_cat/', edit_cat, name='edit_cat'),
    path('edit_app/', edit_app, name='edit_app'),
    path('doc_view/', doc_view, name='doc_view'),
    path('rejection_app/<int:id>', rejection_app, name='rejection_app'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)