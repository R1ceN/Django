from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Employee
from .models import Shiiregyosha


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
            Employee.objects.create(empid=empid, empfname=empfname, emplname=emplname, emppasswd=password,
                                    emprole=emprole)
            return HttpResponse('従業員が登録されました。')
        except Exception as e:
            return render(request, '従業員登録.html', {'error': str(e)})

    return render(request, '従業員登録.html')


def supplier_menu(request):
    return render(request, '仕入れ.html')


def search_by_capital(request):
    suppliers = None
    if request.method == 'POST':
        capital = request.POST.get('capital')
        if capital:
            try:
                capital_value = int(capital)
                suppliers = Shiiregyosha.objects.filter(shihonkin__gte=capital_value)
            except ValueError:
                suppliers = []

    return render(request, '資本金検索.html', {'suppliers': suppliers})


def update_supplier_phone(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        new_phone = request.POST.get('phone')
        try:
            supplier = Shiiregyosha.objects.get(shiireid=supplier_id)
            supplier.shiiretel = new_phone
            supplier.save()
            return HttpResponse('電話番号が更新されました。')
        except Shiiregyosha.DoesNotExist:
            return HttpResponse('仕入れ先が見つかりませんでした。')
    return render(request, '電話番号変更.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee


def change_employee_name(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        new_fname = request.POST.get('new_fname')
        new_lname = request.POST.get('new_lname')

        try:
            employee = Employee.objects.get(empid=employee_id)
            employee.empfname = new_fname
            employee.emplname = new_lname
            employee.save()
            messages.success(request, '従業員の氏名が正常に更新されました。')
        except Employee.DoesNotExist:
            messages.error(request, '従業員IDが見つかりません。')

        return redirect('change_employee_name')

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
