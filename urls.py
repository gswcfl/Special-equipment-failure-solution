from django.conf.urls.defaults import patterns,include,url
from check_site import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^site_project/', include('site_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^index/$',views.index),
	(r'^query/$',views.query),
	(r'^change/$',views.change),
	(r'^sugon_change/$',views.sugon_change),
	(r'top',views.top),
	(r'right',views.right),
	(r'left',views.left),
	(r'buttom',views.buttom),
	(r'manage_host',views.manage_host),
	(r'^upload_file/$',views.upload_file),
	(r'^query_passwd/$',views.query_passwd),
)
