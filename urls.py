from django.conf.urls.defaults import *
from map.views import index, rip, test, all_routes, feedback, nearest, all_bus_stops, companies, orangeCompanies, routes
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^icity/', include('icity.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    ('^$', index),
    (r'^rip$', rip),
    (r'^test.xml$', test),
    (r'^all_routes.xml$', all_routes),
    (r'^all_bus_stops.xml$', all_bus_stops),
    (r'^feedback/$', feedback),
    (r'^nearest/$', nearest),
    (r'^companies/(\d{6})', companies),
    (r'^orange-companies/(\d{6})', orangeCompanies),
    (r'^routes/(\d{1,3}).xml', routes),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                            )