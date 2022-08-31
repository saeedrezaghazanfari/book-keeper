from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from Extentions.utils import user_image_path


class User(AbstractUser):
    ip_address = models.GenericIPAddressField(protocol='both', blank=True, null=True, verbose_name=_('آیپی'))
    profile = models.ImageField(upload_to=user_image_path, null=True, blank=True, verbose_name=_('پروفایل'))
    is_guest = models.BooleanField(default=False, verbose_name=_('آیا این کاربر مهمان است؟'))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    get_full_name.short_description = _('نام و نام خانوادگی')

    class Meta:
        ordering = ['-id']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')