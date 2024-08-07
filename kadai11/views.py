import re
from datetime import datetime
from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from kadai11.models import Appointment, Doctor
from kadai11.models import Employee, Patient, Shiiregyosha, Medicine, Treatment, Tabyouin

from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        password = request.POST.get('password')
        if not empid or not password:
            return render(request, 'login.html', {'error': 'Please enter both Employee ID and Password'})

        try:
            user = Employee.objects.get(empid=empid)
            if password.strip() == user.emppasswd.strip():  # ハッシュ化を行わずに直接比較
                request.session['user_id'] = user.empid  # セッションにユーザーIDを保存
                request.session['is_authenticated'] = True  # セッションに認証状態を保存
                request.session['user_role'] = user.emprole  # セッションにユーザーの役割を保存
                if user.emprole == 1:  # 管理者
                    return render(request, '管理者.html')
                elif user.emprole == 2:  # 受付
                    return render(request, '従業員受付.html')
                elif user.emprole == 3:  # 医師
                    return render(request, '従業員医師.html')
                else:
                    return redirect(reverse('home'))
            else:
                return render(request, 'login.html', {'error': '認証情報が無効です'})
        except Employee.DoesNotExist:
            return render(request, 'login.html', {'error': 'ユーザーが存在しません'})
        except Exception as e:
            return render(request, 'login.html', {'error': f'エラーが発生しました: {e}'})
    return render(request, 'login.html')


def check_session(request):
    print("User ID:", request.session.get('user_id'))
    print("Is Authenticated:", request.session.get('is_authenticated'))
    print("User Role:", request.session.get('user_role'))

    request.session.modified = True

    return JsonResponse({
        'user_id': request.session.get('user_id'),
        'is_authenticated': request.session.get('is_authenticated'),
        'user_role': request.session.get('user_role')
    })

def logout_view(request):
    auth_logout(request)
    return redirect('login')


# デコレータの作成
def login_required(role=None):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.session.get('is_authenticated', False):
                return redirect('login')
            if role and str(request.session.get('user_role')) != str(role):
                return render(request, 'アクセス拒否.html')
            return function(request, *args, **kwargs)

        return wrap

    return decorator


@login_required(role='1')
def admin_page(request):
    return render(request, '管理者.html')


@login_required(role='1')
def register_employee(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        empfname = request.POST.get('firstName')
        emplname = request.POST.get('lastName')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        emprole = request.POST.get('role')

        if password != confirm_password:
            return render(request, '従業員登録.html', {'error': 'パスワードが違います。'})

        try:
            if Employee.objects.filter(empid=empid).exists():
                return render(request, '従業員登録.html',
                              {'error': '従業員IDは既に存在します。別のIDを入力してください。'})

            Employee.objects.create(empid=empid, empfname=empfname, emplname=emplname,
                                    emppasswd=password, emprole=emprole)
            return render(request, '登録成功.html')  # 登録成功テンプレートをレンダリング
        except Exception as e:
            return render(request, '従業員登録.html', {'error': str(e)})

    return render(request, '従業員登録.html')


@login_required(role='1')
def tabyouin_page(request):
    return render(request, '他病院.html')


@login_required(role='1')
def register_tabyouin(request):
    if request.method == 'POST':
        tabyouinid = request.POST.get('tabyouinid').strip()
        tabyouinmei = request.POST.get('tabyouinmei').strip()
        tabyouinaddress = request.POST.get('tabyouinaddress').strip()
        tabyouintel = request.POST.get('tabyouintel').strip()
        tabyouinshihonkin = request.POST.get('tabyouinshihonkin').strip()
        kyukyu = request.POST.get('kyukyu').strip()

        errors = []
        tabyouinshihonkin_value = None

        # 全項目が空欄の場合
        if not (tabyouinid and tabyouinmei and tabyouinaddress and tabyouintel and tabyouinshihonkin and kyukyu):
            errors.append("すべての項目を入力してください。")

        # 重複IDのチェック
        if Tabyouin.objects.filter(tabyouinid=tabyouinid).exists():
            errors.append("この他病院IDは既に存在します。別のIDを入力してください。")

        # 電話番号のバリデーション
        if not re.match(r'^[0-9()-]+$', tabyouintel):
            errors.append('電話番号には数字、ハイフン、括弧のみを使用してください。')

        # 資本金のバリデーション
        try:
            tabyouinshihonkin_value = int(tabyouinshihonkin.replace('￥', '').replace(',', ''))
            if tabyouinshihonkin_value < 1:
                errors.append('資本金は1以上の数値を入力してください。')
        except ValueError:
            errors.append('資本金には数値、カンマ、円記号のみを使用してください。')

        # 救急対応のバリデーション
        if kyukyu not in ['1', '0']:
            errors.append('救急対応は1（救急対応）または0（他対応）で入力してください。')

        if errors:
            return render(request, '他病院登録機能.html', {'errors': errors})

        try:
            Tabyouin.objects.create(
                tabyouinid=tabyouinid,
                tabyouinmei=tabyouinmei,
                tabyouinaddress=tabyouinaddress,
                tabyouintel=tabyouintel,
                tabyouinshihonkin=tabyouinshihonkin_value,
                kyukyu=kyukyu
            )
            messages.success(request, '他病院が正常に登録されました')
            return redirect('tabyouin_list')  # 登録完了テンプレートをレンダリングする代わりにリストページにリダイレクト
        except Exception as e:
            errors.append(f'他病院の登録に失敗しました: {str(e)}')
            return render(request, '他病院登録機能.html', {'errors': errors})

    return render(request, '他病院登録機能.html')


@login_required(role='1')
# 他病院の一覧表示
def tabyouin_list(request):
    tabyouins = Tabyouin.objects.all()
    return render(request, '他病院一覧表示機能.html', {'tabyouins': tabyouins})


@login_required(role='1')
# 他病院の住所検索
def search_tabyouin_by_address(request):
    tabyouins = None
    address_query = ''
    if request.method == 'POST':
        address_query = request.POST.get('address', '')
        if address_query:
            tabyouins = Tabyouin.objects.filter(tabyouinaddress__icontains=address_query)
    return render(request, '他病院住所検索機能.html', {'tabyouins': tabyouins, 'query': address_query})


@login_required(role='1')
def search_tabyouin_by_capital(request):
    tabyouins = None
    capital_query = ''
    if request.method == 'POST':
        capital_query = request.POST.get('capital', '')
        if capital_query:
            try:
                # 「￥」、「円」、カンマを削除して数値に変換
                cleaned_query = re.sub(r'[￥¥円,]', '', capital_query)
                capital_value = int(cleaned_query)
                if capital_value < 1:
                    raise ValueError("Capital must be 1 or greater.")
                tabyouins = Tabyouin.objects.filter(tabyouinshihonkin__gte=capital_value)
            except ValueError:
                tabyouins = []
                messages.error(request, '資本金は1以上の数値を入力してください。')
    return render(request, '他病院資本金検索機能.html', {'tabyouins': tabyouins, 'query': capital_query})


@login_required(role='1')
# 他病院の電話番号変更
def update_tabyouin_phone(request):
    if request.method == 'POST':
        tabyouin_id = request.POST.get('tabyouin_id')
        new_phone = request.POST.get('phone')
        try:
            tabyouin = Tabyouin.objects.get(tabyouinid=tabyouin_id)
            tabyouin.tabyouintel = new_phone
            tabyouin.save()
            messages.success(request, '電話番号が正常に更新されました')
            return redirect('tabyouin_list')
        except Tabyouin.DoesNotExist:
            messages.error(request, '他病院が見つかりませんでした')
    return render(request, '他病院情報変更機能.html')


@login_required(role='1')
def supplier_menu(request):
    return render(request, '仕入れ.html')


@login_required(role='1')
def update_supplier_phone(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier_id')
        new_phone = request.POST.get('phone')

        errors = []

        # 電話番号のバリデーション
        if not re.match(r'^[0-9()-]+$', new_phone):
            errors.append('電話番号には数字、ハイフン、括弧のみを使用してください。')

        cleaned_phone = new_phone.replace('-', '').replace('(', '').replace(')', '')

        # Validate length of the phone number
        if len(cleaned_phone) < 11 or len(cleaned_phone) > 12:
            errors.append('電話番号は11桁または12桁である必要があります。')

        if errors:
            return render(request, '電話番号変更.html', {'errors': errors})

        try:
            supplier = Shiiregyosha.objects.get(shiireid=supplier_id)
            supplier.shiiretel = new_phone
            supplier.save()
            return render(request, '更新成功.html')  # 更新成功テンプレートをレンダリング
        except Shiiregyosha.DoesNotExist:
            return render(request, '電話番号変更.html', {'errors': ['仕入れ先が見つかりませんでした。']})
    return render(request, '電話番号変更.html')


@login_required(role='1')
def search_by_capital(request):
    suppliers = None
    capital_query = ''
    if request.method == 'POST':
        capital_query = request.POST.get('capital', '')
        if capital_query:
            try:
                # 「￥」と「円」、カンマを削除して数値に変換
                cleaned_query = re.sub(r'[￥¥円,]', '', capital_query)
                capital_value = int(cleaned_query)
                if capital_value < 1:
                    raise ValueError("Capital must be 1 or greater.")
                suppliers = Shiiregyosha.objects.filter(shihonkin__gte=capital_value)
            except ValueError:
                suppliers = []
                messages.error(request, '資本金は1以上の数値を入力してください。')
    return render(request, '資本金検索.html', {'suppliers': suppliers, 'query': capital_query})


@login_required(role='1')
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
            return render(request, '従業員氏名変更完了.html')
        except Employee.DoesNotExist:
            messages.error(request, '従業員IDが見つかりません。')

        return redirect('change_employee_name')

    return render(request, '従業員氏名変更.html')


@login_required(role='1')
def add_supplier(request):
    if request.method == 'POST':
        shiireid = request.POST.get('shiireid').strip()
        shiiremei = request.POST.get('shiiremei').strip()
        shiireaddress = request.POST.get('shiireaddress').strip()
        shiiretel = request.POST.get('shiiretel').strip()
        shihonkin = request.POST.get('shihonkin').strip()
        nouki = request.POST.get('nouki').strip()

        errors = []
        shihonkin_value = None
        nouki_value = None

        # 全項目が空欄の場合
        if not (shiireid and shiiremei and shiireaddress and shiiretel and shihonkin and nouki):
            errors.append("すべての項目を入力してください。")

        # 重複IDのチェック
        if Shiiregyosha.objects.filter(shiireid=shiireid).exists():
            errors.append("この仕入先IDは既に存在します。別のIDを入力してください。")

        # 電話番号のバリデーション
        if not re.match(r'^[0-9()-]+$', shiiretel):
            errors.append('電話番号には数字、ハイフン、括弧のみを使用してください。')

        # 資本金のバリデーション
        try:
            shihonkin_value = int(shihonkin.replace('￥', '').replace(',', ''))
            if shihonkin_value < 1:
                errors.append('資本金は1以上の数値を入力してください。')
        except ValueError:
            errors.append('資本金には数値、カンマ、円記号のみを使用してください。')

        # 納期のバリデーション
        try:
            nouki_value = int(nouki)
            if nouki_value < 1:
                errors.append('納期は1日以上の数値を入力してください。')
        except ValueError:
            errors.append('納期には数値のみを使用してください。')

        if errors:
            return render(request, '仕入れ先追加.html', {'errors': errors})

        try:
            Shiiregyosha.objects.create(
                shiireid=shiireid,
                shiiremei=shiiremei,
                shiireaddress=shiireaddress,
                shiiretel=shiiretel,
                shihonkin=shihonkin_value,
                nouki=nouki_value
            )
            return render(request, '仕入れ先追加完了.html')  # 登録完了テンプレートをレンダリング
        except Exception as e:
            messages.error(request, f'仕入先の追加に失敗しました: {str(e)}')

        return redirect('add_supplier')

    return render(request, '仕入れ先追加.html')


@login_required(role='1')
def supplier_list(request):
    suppliers = Shiiregyosha.objects.all()
    return render(request, '仕入れ先一覧.html', {'suppliers': suppliers})


@login_required(role='2')
def employee_reception(request):
    if not request.user.is_staff:
        return redirect('login')
    appointments = Appointment.objects.all()
    return render(request, '従業員受付.html', {'appointments': appointments})


@login_required(role='3')
def employee_doctor(request):
    if not request.user.groups.filter(name='Doctors').exists():
        return redirect('login')
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date=timezone.now().date())
    return render(request, '従業員医師.html', {'appointments': appointments})


@login_required(role='2')
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
                return render(request, '受付情報変更.html')  # 登録完了テンプレートをレンダリング
        except Employee.DoesNotExist:
            messages.error(request, 'ユーザーが見つかりません。')
        except Exception as e:
            messages.error(request, f'エラーが発生しました: {str(e)}')

    return render(request, '従業員情報変更ps.html')


@login_required(role='3')
def change_password1(request):
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
                return render(request, '医師情報変更.html')  # 登録完了テンプレートをレンダリング
        except Employee.DoesNotExist:
            messages.error(request, 'ユーザーが見つかりません。')
        except Exception as e:
            messages.error(request, f'エラーが発生しました: {str(e)}')

    return render(request, '従業員情報変更ps1.html')


@login_required(role='2')
def register_patient(request):
    if request.method == 'POST':
        patid = request.POST.get('patid')
        patfname = request.POST.get('patfname')
        patlname = request.POST.get('patlname')
        hokenmei = request.POST.get('hokenmei')
        hokenexp = request.POST.get('hokenexp')

        try:
            # 患者IDが既に存在するかチェック
            if Patient.objects.filter(patid=patid).exists():
                messages.error(request, 'この患者IDは既に存在します。別のIDを入力してください。')
                return render(request, '患者登録.html')

            # 有効期限の検証
            expiration_date = datetime.strptime(hokenexp, '%Y-%m-%d')
            if expiration_date <= datetime.now():
                messages.error(request, '有効期限は未来の日付を入力してください。')
                return render(request, '患者登録.html')

            Patient.objects.create(patid=patid, patfname=patfname, patlname=patlname,
                                   hokenmei=hokenmei, hokenexp=hokenexp)
            messages.success(request, '患者が正常に登録されました。')
            return render(request, '登録完了.html')  # 登録完了テンプレートをレンダリング
        except Exception as e:
            messages.error(request, f'患者の登録に失敗しました: {e}')

    return render(request, '患者登録.html')


@login_required(role='2')
def get_insurance_number(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patientID')
        try:
            patient = Patient.objects.get(patid=patient_id)
            return JsonResponse({
                'insuranceNumber': patient.hokenmei,
                'insuranceExpiration': patient.hokenexp.strftime('%Y-%m-%d')
            })
        except Patient.DoesNotExist:
            return JsonResponse({'insuranceNumber': '', 'insuranceExpiration': ''})
    return JsonResponse({'error': '無効なリクエストです。'}, status=400)


@login_required(role='2')
def get_patient_ids(request):
    if request.method == 'GET':
        patients = Patient.objects.values_list('patid', flat=True)
        return JsonResponse(list(patients), safe=False)
    return JsonResponse({'error': '無効なリクエストです。'}, status=400)


@login_required(role='2')
def update_insurance(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patientID')
        insurance_number = request.POST.get('insuranceNumber')
        insurance_expiration = request.POST.get('insuranceExpiration')

        try:
            patient = Patient.objects.get(patid=patient_id)

            # 保険証記号番号のバリデーション
            if insurance_number and (
                    len(insurance_number) != 10 or not insurance_number[:8].isalnum() or not insurance_number[
                                                                                             8:].isdigit()):
                messages.error(request, '保険証記号番号は英数字8桁+数字2桁の10桁で入力してください。')
                return render(request, '患者保険証変更.html', {'patients': Patient.objects.all()})

            if insurance_number:
                patient.hokenmei = insurance_number

            if insurance_expiration:
                new_expiration_date = datetime.strptime(insurance_expiration, '%Y-%m-%d').date()
                current_expiration_date = patient.hokenexp

                if new_expiration_date <= current_expiration_date:
                    messages.error(request, '新しい有効期限は現在の有効期限より後の日付を入力してください。')
                    return render(request, '患者保険証変更.html', {'patients': Patient.objects.all()})

                if new_expiration_date.month == 2 and new_expiration_date.day == 29:
                    if not (new_expiration_date.year % 4 == 0 and (
                            new_expiration_date.year % 100 != 0 or new_expiration_date.year % 400 == 0)):
                        messages.error(request, '指定された日付は有効なうるう年の日付ではありません。')
                        return render(request, '患者保険証変更.html', {'patients': Patient.objects.all()})
                patient.hokenexp = new_expiration_date

            patient.save()
            messages.success(request, '保険証情報が正常に更新されました。')
            return redirect('update_insurance')
        except Patient.DoesNotExist:
            messages.error(request, '患者が見つかりません。')
        except Exception as e:
            messages.error(request, f'保険証情報の更新に失敗しました: {e}')

    return render(request, '患者保険証変更.html', {'patients': Patient.objects.all()})


@login_required(role='2')
def search_expired_insurance(request):
    patients = []
    if request.method == 'POST':
        insurance_expiration = request.POST.get('insuranceExpiration')
        patients = Patient.objects.filter(hokenexp__lt=insurance_expiration)

    return render(request, '患者検索期限切れ.html', {'patients': patients})


@login_required(role='2')
def search_patients(request):
    search_type = request.GET.get('search_type')
    search_value = request.GET.get('search_value')
    patients = []

    if search_type == 'all':
        patients = Patient.objects.all()
    elif search_type == 'id':
        patients = Patient.objects.filter(patid__icontains=search_value)
    elif search_type == 'name':
        patients = Patient.objects.filter(patfname__icontains=search_value) | Patient.objects.filter(
            patlname__icontains=search_value)

    return render(request, '患者検索（全件）.html', {'patients': patients})


# 一時的な指示リストをセッションから取得
def get_temporary_instructions(request):
    return request.session.get('temporary_instructions', [])


# 一時的な指示リストをセッションに保存
def save_temporary_instructions(request, instructions):
    request.session['temporary_instructions'] = instructions


@login_required(role='3')
def drug_administration_instructions(request):
    medicines = Medicine.objects.all()
    patients = Patient.objects.all()
    temporary_instructions = get_temporary_instructions(request)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        medicine_id = request.POST.get('medicine')
        quantity = request.POST.get('quantity')

        if not quantity.isdigit() or int(quantity) <= 0:
            messages.error(request, '数量は正の整数で1より大きい必要があります。')
        else:
            try:
                patient = Patient.objects.get(patid=patient_id)
                medicine = Medicine.objects.get(medicineid=medicine_id)
                temporary_instructions.append({
                    'patient': patient.patid,
                    'patfname': patient.patfname,
                    'patlname': patient.patlname,
                    'hokenmei': patient.hokenmei,
                    'medicine': medicine.medicineid,
                    'medicinename': medicine.medicinename,
                    'unit': medicine.unit,
                    'quantity': int(quantity),
                    'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                save_temporary_instructions(request, temporary_instructions)
                messages.success(request, '薬剤投与指示が一時的に追加されました。')
                return render(request, '処置追加.html')
            except Patient.DoesNotExist:
                messages.error(request, '患者が見つかりません。')
            except Medicine.DoesNotExist:
                messages.error(request, '薬剤が見つかりません。')

        return redirect('drug_administration_instructions')

    return render(request, '薬投与指示.html', {
        'medicines': medicines,
        'patients': patients,
        'instructions': temporary_instructions
    })


@login_required(role='3')
def drug_administration_confirm(request):
    temporary_instructions = get_temporary_instructions(request)
    if request.method == 'POST':
        if 'delete' in request.POST:
            index = int(request.POST.get('delete'))
            if 0 <= index < len(temporary_instructions):
                del temporary_instructions[index]
                save_temporary_instructions(request, temporary_instructions)
                messages.success(request, '薬剤投与指示が削除されました。')
            else:
                messages.error(request, '無効なインデックスです。')
        elif 'update_all' in request.POST:
            quantities = request.POST.getlist('quantities')
            indices = request.POST.getlist('indices')
            for i, index in enumerate(indices):
                idx = int(index)
                new_quantity = int(quantities[i])
                if 0 <= idx < len(temporary_instructions) and new_quantity > 0:
                    temporary_instructions[idx]['quantity'] = new_quantity
                else:
                    messages.error(request, '無効なインデックスまたは数量です。')
            save_temporary_instructions(request, temporary_instructions)
            messages.success(request, '数量が更新されました。')
        elif 'confirm' in request.POST:
            user_id = request.session.get('user_id')
            employee = Employee.objects.get(empid=user_id)
            for instruction in temporary_instructions:
                patient = Patient.objects.get(patid=instruction['patient'])
                medicine = Medicine.objects.get(medicineid=instruction['medicine'])
                Treatment.objects.create(
                    patient=patient,
                    medicine=medicine,
                    employee=employee,  # 従業員情報を保存
                    quantity=instruction['quantity'],
                    confirmed_at=timezone.now()
                )
            temporary_instructions.clear()
            save_temporary_instructions(request, temporary_instructions)
            messages.success(request, '処置が確定されました。')
            return render(request, '処置確定.html')  # 成功テンプレートをレンダリング

    return render(request, '薬投与削除・確定.html', {
        'instructions': temporary_instructions
    })


@login_required(role='3')
def history_display(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')

        try:
            patient = Patient.objects.get(patid=patient_id)
            confirmed_instructions = Treatment.objects.filter(patient=patient)

            if confirmed_instructions.exists():
                return render(request, '履歴表示.html', {'confirmed_instructions': confirmed_instructions})
            else:
                messages.info(request, 'この患者には処置履歴がありません。')
                return render(request, '履歴表示.html', {'confirmed_instructions': []})

        except Patient.DoesNotExist:
            messages.error(request, '患者IDが見つかりません。')
            return render(request, '履歴表示.html', {'confirmed_instructions': []})

    return render(request, '履歴表示.html', {'confirmed_instructions': []})