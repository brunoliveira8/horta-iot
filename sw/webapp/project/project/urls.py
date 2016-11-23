from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.forms import RegistrationForm
from registration.backends.simple.views import RegistrationView
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('app.urls')),
    url(r'admin/', include(admin.site.urls)),
    url(r'accounts/register/$', RegistrationView.as_view(form_class = RegistrationForm), name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)


# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )