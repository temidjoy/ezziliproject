"""
Definition of urls for EzziliProject.
"""

from django.conf.urls import patterns, include, url
from EzziliApp.views import AdvertsPhotos, AdvertDataView, PhotoList, Photodetail, AdvertDetails, PropertyAdvertDetails, BasicAdvertDetails

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from EzziliProject import settings

admin.autodiscover()


photourls = patterns('',
                     url(r'^$', PhotoList.as_view(), name='photo-list'),
                     url(r'^/(?P<pk>\d+)$', Photodetail.as_view(), name='Photo-list'))
urlpatterns = patterns('', url(r'^(?P<pk>\d+)/photos$', AdvertsPhotos.as_view(), name='advertphoto-list'),
                                 
    # Examples:
    # url(r'^$', 'EzziliProject.views.home', name='home'),
    # url(r'^EzziliProject/', include('EzziliProject.EzziliProject.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^photos', include(photourls)),
     url(r'^account/', include('account_api.urls')),
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$',AdvertDataView.as_view(), name='Advert-list'),
      url(r'^advert/(?P<pk>\d+)/facdetails$', AdvertDetails.as_view(), name='Facility-list'),
       url(r'^advert/(?P<pk>\d+)/propertydetails$', PropertyAdvertDetails.as_view(), name='Property-list'),
        url(r'^advert/(?P<pk>\d+)/basicinfodetails$', BasicAdvertDetails.as_view(), name='Basic-list'),
     url(r'^(?P<pk>\d+)/photos$', AdvertsPhotos.as_view(), name='advertphoto-list'),


)
