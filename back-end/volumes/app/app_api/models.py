from django.db import models
from app_auth.models import User 
from Extentions.utils import user_image_path
from django.utils.translation import gettext_lazy as _


class TransactionModel(models.Model):
    BUYSELLOPTION = (('withdrawal', _('برداشت')), ('deposit', _('واریز')))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('کاربر'))
    card = models.ForeignKey('BankModel', on_delete=models.CASCADE, verbose_name=_('کارت بانکی'))
    price = models.FloatField(verbose_name=_('مبلغ'))
    in_out = models.CharField(choices=BUYSELLOPTION, max_length=20, verbose_name=_('واریز یا برداشت؟'))
    description = models.TextField(verbose_name=_('توضیحات'))
    time = models.TimeField(verbose_name=_('زمان'))
    date = models.DateField(blank=True, null=True, verbose_name=_('تاریخ'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('تراکنش')
        verbose_name_plural = _('تراکنش ها')
    
    def __str__(self):  
        if self.user.first_name:
            return self.user.first_name + ' ' + self.user.last_name
        return str(self.id)

class BankModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('کاربر'))
    name = models.CharField(max_length=255, verbose_name=_('نام بانک'))
    card_number = models.BigIntegerField(verbose_name=_('شماره کارت'))
    stock = models.FloatField(verbose_name=_('موجودی'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('کارت بانکی')
        verbose_name_plural = _('کارت های بانکی')
    
    def __str__(self):  
        if self.user.first_name:
            return self.user.first_name + ' ' + self.user.last_name + f' ({self.name})'
        return str(self.id)


class ProfileCollectorModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('کاربر'))
    profile = models.ImageField(upload_to=user_image_path, null=True, blank=True, verbose_name=_('پروفایل'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('جمع آورنده ی پروفایل')
        verbose_name_plural = _('جمع آورنده ی پروفایل کاربران')
    
    def __str__(self):
        return str(self.id)


class VersionsModel(models.Model):
    version = models.CharField(max_length=255, verbose_name=_('ورژن'))
    description = models.TextField(verbose_name=_('توضیحات ورژن'))

    class Meta:
        ordering = ['id']
        verbose_name = _('ورژن')
        verbose_name_plural = _('ورژن‌ها')
    
    def __str__(self):
        return self.version