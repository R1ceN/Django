from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Employee


def login(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        password = request.POST['password']
        user = Employee.objects.get(empid=empid)
        if user is not None:
            print(user.emprole)
            if user.emprole == 1:  # 管理者
                return render(request, '管理者.html')
            elif user.emprole == 2:  # 受付
                return render(request, '従業員受付.html')
            elif user.emprole == 3:  # 医師
                return render(request, '従業員医師.html')
            else:
                return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def Admin(request):
    return render(request, '管理者.html')


def register_employee(request):
    if request.method == 'POST':
        empfname = request.POST.get('firstName')
        emplname = request.POST.get('lastName')
        email = request.POST.get('email')
        empid = email.split('@')[0]  # emailの@より前をempidとして使用
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        emprole = request.POST.get('role')

        if password != confirm_password:
            return render(request, '従業員登録.html', {'error': 'Passwords do not match'})

        try:
            Employee.objects.create(empid=empid, empfname=empfname, emplname=emplname, emppasswd=password, emprole=emprole)
            return HttpResponse('従業員が登録されました。')
        except Exception as e:
            return render(request, '従業員登録.html', {'error': str(e)})

    return render(request, '従業員登録.html')


def SupplierList(request):
    return render(request, '仕入れ.html')


def CapitalSearch(request):
    return render(request, '資本金検索.html')


def UpdateSupplierPhone(request):
    return render(request, '電話番号変更.html')


def EmployeeNameChange(request):
    return render(request, '従業員氏名変更.html')


def EmployeeReception(request):
    return render(request, '従業員受付.html')


def EmployeeDoctor(request):
    return render(request, '従業員医師.html')


def ChangeEmployeeInformation(request):
    return render(request, '従業員情報変更ps.html')


def PatientRegistration(request):
    return render(request, '患者登録.html')


def PatientManagement(request):
    return render(request, '患者管理.html')


def PatientSearchExpired(request):
    return render(request, '患者検索期限切れ.html')


def PatientSearchAll(request):
    return render(request, '患者検索（全件）.html')


def DrugAdministrationInstructions(request):
    return render(request, '薬投与指示.html')


def DrugAdministrationConfirmed(request):
    return render(request, '薬投与確定.html')


def HistoryDisplay(request):
    return render(request, '履歴表示.html')
