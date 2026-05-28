from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("about/", views.about_tax, name="about_tax"),
	path("about/salary/", views.about_salary_tax, name="about_salary_tax"),
	path("about/property/", views.about_property_tax, name="about_property_tax"),
	path("about/vat/", views.about_vat_tax, name="about_vat_tax"),
	path("about/income/", views.about_income_tax, name="about_income_tax"),
	path("about/withholding/", views.about_withholding_tax, name="about_withholding_tax"),
    path("about/patent/", views.about_patent_tax, name="about_patent_tax"),
	path("about/special/", views.about_special_tax, name="about_special_tax"),
    path("about/registration/", views.about_registration_tax, name="about_registration_tax"),
    path("about/unused-land/", views.about_unused_land_tax, name="about_unused_land_tax"),
	path("salary/", views.salary_tax, name="salary_tax"),
	path("property/", views.property_tax, name="property_tax"),	
	path("vat/", views.vat_tax, name="vat_tax"),
	path("income/", views.income_tax, name="income_tax"),
	path("withholding/", views.withholding_tax, name="withholding_tax"),
	path("patent/", views.patent_tax, name="patent_tax"),
	path("special/", views.special_tax, name="special_tax"),
	path("registration/", views.registration_tax, name="registration_tax"),
	path("unused-land/", views.unused_land_tax, name="unused_land_tax"),
	path("admin/records/", views.admin_records, name="admin_records"),
	path("study-plan/", views.study_plan, name="study_plan"),
	path("about/accomodation-tax/", views.about_accomodation_tax, name="about_accomodation_tax"),
	path("accomodation-tax/", views.accomodation_tax, name="accomodation_tax"),
	path("about/special-tax/", views.about_special_tax, name="about_special_tax"),
	path("special-tax/", views.special_tax, name="special_tax"),
]
