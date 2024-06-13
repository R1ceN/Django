from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('admin_page/', views.Admin, name='Admin'),
    path('employeeregistration/', views.EmployeeRegistration, name='EmployeeRegistration'),
    path('supplierlist/', views.SupplierList, name='SupplierList'),
    path('capitalsearch/', views.CapitalSearch, name='CapitalSearch'),
    path('updatesupplierphone/', views.UpdateSupplierPhone, name='UpdateSupplierPhone'),
    path('employeenamechange/', views.EmployeeNameChange, name='EmployeeNameChange'),
    path('employeereception/', views.EmployeeReception, name='EmployeeReception'),
    path('employeedoctor/', views.EmployeeDoctor, name='EmployeeDoctor'),
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
