from django.db import models
from django.utils import timezone


class Tabyouin(models.Model):
    tabyouinid = models.CharField(max_length=8, primary_key=True)
    tabyouinmei = models.CharField(max_length=64)
    tabyouinaddress = models.CharField(max_length=64)
    tabyouintel = models.CharField(max_length=13)
    tabyouinshihonkin = models.IntegerField()
    kyukyu = models.IntegerField()  # 1: 救急対応, それ以外: 非対応


class Shiiregyosha(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True)
    shiiremei = models.CharField(max_length=64)
    shiireaddress = models.CharField(max_length=64)
    shiiretel = models.CharField(max_length=13)
    shihonkin = models.IntegerField()
    nouki = models.IntegerField()  # 発注して届く日数


class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=128)  # ハッシュデータを保存
    emprole = models.IntegerField()  # 受付 or 医師の識別


class Patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True)
    patfname = models.CharField(max_length=64)
    patlname = models.CharField(max_length=64)
    hokenmei = models.CharField(max_length=64)  # 保険証名記号番号
    hokenexp = models.DateField()  # 有効期限


class Medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)  # 枚・ml・本など

class Treatment(models.Model):
    treatmentid = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=1)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    confirmed_at = models.DateTimeField(default=timezone.now, null=False)