from django.conf.urls import patterns, include, url



urlpatterns = patterns('chat',
    # Examples:
    # url(r'^$', 'teamgames_services.views.home', name='home'),
    url(r'get_team/$', 'views.get_team',)

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)