from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == 'admin':
                return redirect(reverse('Admin'))
            elif user.role == 'receptionist':
                return redirect(reverse('EmployeeReception'))
            elif user.role == 'doctor':
                return redirect(reverse('EmployeeDoctor'))
            else:
                return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def Admin(request):
    return render(request, '管理者.html')


def EmployeeRegistration(request):
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
