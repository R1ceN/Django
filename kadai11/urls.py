from django.urls import path
from . import views
from .views import admin_page


urlpatterns = [
    path('admin_page/', admin_page, name='admin_page'),  # 管理者ページのURLパスとビュー
    path('login/', views.login, name='login'),
    path('register/', views.register_employee, name='register_employee'),
    path('employee_reception/', views.employee_reception, name='employee_reception'),
    path('employee_doctor/', views.employee_doctor, name='employee_doctor'),
    path('supplier/', views.supplier_menu, name='supplier_menu'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('check_session/', views.check_session, name='check_session'),
    path('update_supplier_phone/', views.update_supplier_phone, name='update_supplier_phone'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('tabyouin_page/', views.tabyouin_page, name='tabyouin_page'),
    path('register_tabyouin/', views.register_tabyouin, name='register_tabyouin'),
    path('tabyouin_list/', views.tabyouin_list, name='tabyouin_list'),
    path('search_tabyouin_by_address/', views.search_tabyouin_by_address, name='search_tabyouin_by_address'),
    path('search_tabyouin_by_capital/', views.search_tabyouin_by_capital, name='search_tabyouin_by_capital'),
    path('update_tabyouin_phone/', views.update_tabyouin_phone, name='update_tabyouin_phone'),
    path('search_by_capital/', views.search_by_capital, name='search_by_capital'),
    path('change_employee_name/', views.change_employee_name, name='change_employee_name'),
    path('change-password/', views.change_password, name='change_password'),
    path('get_insurance_number', views.get_insurance_number, name='get_insurance_number'),
    path('get_patient_ids', views.get_patient_ids, name='get_patient_ids'),
    path('change-password1/', views.change_password1, name='change_password1'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('update_insurance/', views.update_insurance, name='update_insurance'),
    path('search_expired_insurance/', views.search_expired_insurance, name='search_expired_insurance'),
    path('search_patients/', views.search_patients, name='search_patients'),
    path('drug_administration_instructions/', views.drug_administration_instructions,
         name='drug_administration_instructions'),
    path('drug_administration_confirm/', views.drug_administration_confirm, name='drug_administration_confirm'),
    path('history_display/', views.history_display, name='history_display'),
]
