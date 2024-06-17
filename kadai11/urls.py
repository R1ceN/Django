from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('admin_panel/', views.Admin, name='Admin'),
    path('register/', views.register_employee, name='register_employee'),
    path('doctor/', views.EmployeeDoctor, name='EmployeeDoctor'),
    path('supplier/', views.supplier_menu, name='supplier_menu'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('search_by_capital/', views.search_by_capital, name='search_by_capital'),
    path('update_supplier_phone/', views.update_supplier_phone, name='update_supplier_phone'),
    path('change_employee_name/', views.change_employee_name, name='change_employee_name'),
    path('changeemployeeinformation/', views.ChangeEmployeeInformation, name='ChangeEmployeeInformation'),
    path('patientregistration/', views.PatientRegistration, name='PatientRegistration'),
    path('patientmanagement/', views.PatientManagement, name='PatientManagement'),
    path('patientsearchexpired/', views.PatientSearchExpired, name='PatientSearchExpired'),
    path('patientsearchall/', views.PatientSearchAll, name='PatientSearchAll'),
    path('drugadministrationinstructions/', views.DrugAdministrationInstructions,
         name='DrugAdministrationInstructions'),
    path('drugadministrationconfirmed/', views.DrugAdministrationConfirmed, name='DrugAdministrationConfirmed'),
    path('historydisplay/', views.HistoryDisplay, name='HistoryDisplay'),
]
