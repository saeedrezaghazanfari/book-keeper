from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('', views.select_lang_redirect),
]

urlpatterns += i18n_patterns(
    # AUTH
    path('api/v1/get-token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/get-token/refresh-token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # APP
    path('', include('app_api.urls')),
    path('change/language/', views.activate_language, name='activate_lang'),

    # ADMIN
    path('admin', views.admin_fake_page),
    path('achille/admin/panel', admin.site.urls),
)

handler404 = 'app_api.views.error_404_view'

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
