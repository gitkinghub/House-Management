from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users import router as users_api_router
from house import router as house_api_router
from task import router as task_api_router
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                # Include oauth2_provider URLs
                path(
                    "oauth2/",
                    include("oauth2_provider.urls", namespace="oauth2_provider"),
                ),
                # Include social auth URLs
                path(
                    "auth/",
                    include("rest_framework_social_oauth2.urls", namespace="social"),
                ),
                # Your user router
                path("accounts/", include(users_api_router.router.urls)),
                # Your house router
                path("house/", include(house_api_router.router.urls)),
                # Your tasklist router
                path("task/", include(task_api_router.router.urls)),
            ]
        ),
    ),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar if in DEBUG mode
if settings.DEBUG:
    urlpatterns.append(path('api-auth/', include('rest_framework.urls')))
