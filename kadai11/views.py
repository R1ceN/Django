from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Employee
from .models import Patient
from .models import Shiiregyosha


def login(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        password = request.POST.get('password')
        if not empid or not password:
            return render(request, 'login.html', {'error': 'Please enter both Employee ID and Password'})

        try:
            user = Employee.objects.get(empid=empid)
            if password == user.emppasswd:  # ハッシュ化を行わずに直接比較
                request.session['user_id'] = user.empid  # セッションにユーザーIDを保存
                request.session['is_authenticated'] = True  # セッションに認証状態を保存
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
        except Employee.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
        except Exception as e:
            return render(request, 'login.html', {'error': f'An error occurred: {e}'})
    return render(request, 'login.html')


def admin(request):
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


def add_supplier(request):
    if request.method == 'POST':
        shiireid = request.POST.get('shiireid')
        shiiremei = request.POST.get('shiiremei')
        shiireaddress = request.POST.get('shiireaddress')
        shiiretel = request.POST.get('shiiretel')
        shihonkin = request.POST.get('shihonkin')
        nouki = request.POST.get('nouki')

        try:
            Shiiregyosha.objects.create(
                shiireid=shiireid,
                shiiremei=shiiremei,
                shiireaddress=shiireaddress,
                shiiretel=shiiretel,
                shihonkin=shihonkin,
                nouki=nouki
            )
            messages.success(request, '仕入先が正常に追加されました。')
        except Exception as e:
            messages.error(request, f'仕入先の追加に失敗しました: {str(e)}')

        return redirect('add_supplier')

    return render(request, '仕入れ先追加.html')


def EmployeeReception(request):
    return render(request, '従業員受付.html')


def EmployeeDoctor(request):
    return render(request, '従業員医師.html')


def change_password(request):
    if not request.session.get('is_authenticated', False):
        return redirect('login')

    user_id = request.session['user_id']

    if request.method == 'POST':
        current_password = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']

        try:
            user = Employee.objects.get(empid=user_id)
            if current_password != user.emppasswd:
                messages.error(request, '現在のパスワードが正しくありません。')
            elif new_password != confirm_password:
                messages.error(request, '新しいパスワードと確認用パスワードが一致しません。')
            elif current_password == new_password:
                messages.error(request, '新しいパスワードは現在のパスワードと異なる必要があります。')
            else:
                user.emppasswd = new_password  # パスワードを平文で保存
                user.save()
                messages.success(request, 'パスワードが正常に変更されました。')
                return redirect('employee_reception' if user.emprole == 2 else 'EmployeeDoctor')
        except Employee.DoesNotExist:
            messages.error(request, 'ユーザーが見つかりません。')
        except Exception as e:
            messages.error(request, f'エラーが発生しました: {str(e)}')

    return render(request, '従業員情報変更ps.html')


def register_patient(request):
    if request.method == 'POST':
        patid = request.POST.get('patid')
        patfname = request.POST.get('patfname')
        patlname = request.POST.get('patlname')
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        try:
            Patient.objects.create(patid=patid, patfname=patfname, patlname=patlname,
                                   hokenmei=hokenmei, hokenexp=hokenexp)
            messages.success(request, '患者が正常に登録されました。')
            return redirect('register_patient')
        except Exception as e:
            messages.error(request, f'患者の登録に失敗しました: {e}')

    return render(request, '患者登録.html')


def update_insurance(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patientID')
        insurance_number = request.POST.get('insuranceNumber')
        insurance_expiration = request.POST.get('insuranceExpiration')

        try:
            patient = Patient.objects.get(patid=patient_id)
            if insurance_number:
                patient.hokenmei = insurance_number
            if insurance_expiration:
                patient.hokenexp = insurance_expiration
            patient.save()
            messages.success(request, '保険証情報が正常に更新されました。')
            return redirect('update_insurance')
        except Patient.DoesNotExist:
            messages.error(request, '患者が見つかりません。')
        except Exception as e:
            messages.error(request, f'保険証情報の更新に失敗しました: {e}')

    return render(request, '患者保険証変更.html')


def search_expired_insurance(request):
    patients = []
    if request.method == 'POST':
        insurance_expiration = request.POST.get('insuranceExpiration')
        patients = Patient.objects.filter(hokenexp__lt=insurance_expiration)

    return render(request, '患者検索期限切れ.html', {'patients': patients})


def PatientSearchAll(request):
    return render(request, '患者検索（全件）.html')


def DrugAdministrationInstructions(request):
    return render(request, '薬投与指示.html')


def DrugAdministrationConfirmed(request):
    return render(request, '薬投与確定.html')


def HistoryDisplay(request):
    return render(request, '履歴表示.html')
