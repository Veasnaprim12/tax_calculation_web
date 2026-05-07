from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("about/", views.about_tax, name="about_tax"),
	path("about/salary/", views.about_salary_tax, name="about_salary_tax"),
	path("about/property/", views.about_property_tax, name="about_property_tax"),
	path("about/vat/", views.about_vat_tax, name="about_vat_tax"),
	path("salary/", views.salary_tax, name="salary_tax"),
	path("property/", views.property_tax, name="property_tax"),
	path("admin/records/", views.admin_records, name="admin_records"),
    path('vat_tax/', views.vat_tax, name='vat_tax'),
	path("study-plan/", views.study_plan, name="study_plan"),
]
