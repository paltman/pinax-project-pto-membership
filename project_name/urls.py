from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

from .views import (
    ContactsView,
    ContactCreateView,
    ContactDeleteView,
    ContactUpdateView,
    SchoolYearList,
    StudentsView,
    StudentCreateView,
    StudentDeleteView,
    StudentUpdateView
)


urlpatterns = patterns(
    "",
    url(r"^$", "{{ project_name }}.views.home", name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^contacts/$", ContactsView.as_view(), name="contacts"),
    url(r"^contacts/(?P<pk>\d+)/delete/$", ContactDeleteView.as_view(), name="contact_delete"),
    url(r"^contacts/(?P<pk>\d+)/edit/$", ContactUpdateView.as_view(), name="contact_edit"),
    url(r"^contacts/add/$", ContactCreateView.as_view(), name="contact_add"),
    url(r"^students/$", StudentsView.as_view(), name="students"),
    url(r"^students/(?P<pk>\d+)/delete/$", StudentDeleteView.as_view(), name="student_delete"),
    url(r"^students/(?P<pk>\d+)/edit/$", StudentUpdateView.as_view(), name="student_edit"),
    url(r"^students/add/$", StudentCreateView.as_view(), name="student_add"),
    url(r"^memberships/$", SchoolYearList.as_view(), name="memberships"),
    url(r"^memberships/(?P<pk>\d+)/charge/$", "{{ project_name }}.views.charge", name="memberships_charge")
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
