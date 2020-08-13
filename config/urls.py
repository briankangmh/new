from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
                                   'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tutee/', include('tutee.urls')),
    path('tutor/', include('tutor.urls')),
    path('chat/', include('chat.urls')),
    path('payment/', include('payment.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Titan Admin"
admin.site.site_title = "Titan Admin"
admin.site.index_title = "Titan Admin"
