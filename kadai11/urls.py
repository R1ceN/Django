from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('admin_panel/', views.admin, name='Admin'),
    path('register/', views.register_employee, name='register_employee'),
    path('employee/reception/', views.EmployeeReception, name='employee_reception'),
    path('employee/doctor/', views.EmployeeDoctor, name='EmployeeDoctor'),
    path('supplier/', views.supplier_menu, name='supplier_menu'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('search_by_capital/', views.search_by_capital, name='search_by_capital'),
    path('update_supplier_phone/', views.update_supplier_phone, name='update_supplier_phone'),
    path('change_employee_name/', views.change_employee_name, name='change_employee_name'),
    path('change-password/', views.change_password, name='change_password'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('update_insurance/', views.update_insurance, name='update_insurance'),
    path('search_expired_insurance/', views.search_expired_insurance, name='search_expired_insurance'),
    path('patientsearchall/', views.PatientSearchAll, name='PatientSearchAll'),
    path('drugadministrationinstructions/', views.DrugAdministrationInstructions,
         name='DrugAdministrationInstructions'),
    path('drugadministrationconfirmed/', views.DrugAdministrationConfirmed, name='DrugAdministrationConfirmed'),
    path('historydisplay/', views.HistoryDisplay, name='HistoryDisplay'),
]
