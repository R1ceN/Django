from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('admin_panel/', views.admin, name='Admin'),
    path('register/', views.register_employee, name='register_employee'),
    path('employee_reception/', views.employee_reception, name='employee_reception'),
    path('employee_doctor/', views.employee_doctor, name='employee_doctor'),
    path('supplier/', views.supplier_menu, name='supplier_menu'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('search_by_capital/', views.search_by_capital, name='search_by_capital'),
    path('update_supplier_phone/', views.update_supplier_phone, name='update_supplier_phone'),
    path('change_employee_name/', views.change_employee_name, name='change_employee_name'),
    path('change-password/', views.change_password, name='change_password'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('update_insurance/', views.update_insurance, name='update_insurance'),
    path('search_expired_insurance/', views.search_expired_insurance, name='search_expired_insurance'),
    path('patient_search_all/', views.PatientSearchAll, name='PatientSearchAll'),
    path('drug_administration_instructions/', views.drug_administration_instructions,
         name='drug_administration_instructions'),
    path('drug_administration_confirm/', views.drug_administration_confirm, name='drug_administration_confirm'),
    path('history_display/', views.history_display, name='history_display'),
]
