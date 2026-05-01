from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("about/", views.about_tax, name="about_tax"),
	path("salary/", views.salary_tax, name="salary_tax"),
	path("property/", views.property_tax, name="property_tax"),
	path("admin/records/", views.admin_records, name="admin_records"),
]
