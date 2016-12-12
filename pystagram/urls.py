from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from rest_framework import routers

from photos.views import PostViewSet

router = routers.DefaultRouter()
router.register(r'photos', PostViewSet)

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login_page',),
    url(r'^logout/$', logout, {'next_page': settings.LOGIN_URL }),
    url(r'^photos/',include('photos.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(
    url(r'',include('social.apps.django_app.urls', namespace='social'))
)
