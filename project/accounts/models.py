from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


SEX = (
    (0, "Женщина"),
    (1, "Мужчина"),
)


class User(AbstractUser):
    username = None
    phone = PhoneNumberField(
        unique=True,
        verbose_name=_('phone'),
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_('email')
    )
    code = models.IntegerField(
        verbose_name=_('code'),
        blank=True,
        unique=True,
        null=True,
        # editable=False,
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=_('last activity'),
    )
    image = models.ImageField(
        upload_to='users/%Y/%m/%d',
        blank=True,
        null=True,
        verbose_name=_('image'),
    )
    address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    sex = models.IntegerField(choices=SEX, default=1, verbose_name=_('Пол'),)
    birthday = models.DateField(blank=True, null=True, validators=[MaxValueValidator(datetime.date.today)])
    bonus = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'[id:{self.id}] {self.get_full_name() or str(self.phone)}'

    def __unicode__(self):
        return self.bonus



class Notification(models.Model):
    name = models.CharField(
        _('заголовок'), 
        max_length=150)
    image = models.ImageField(
        _('изображение'),
        upload_to='notification_images/',
        null=True, 
        blank=True
        )
    content = models.CharField(_('контент'), max_length=500)
    is_read = models.BooleanField(_('прочитано'), default=False)
    user = models.ForeignKey(
        User, 
        models.CASCADE, 
        'notifications', 
        verbose_name=_('пользователь'),
        blank=True,
        null=True
        )
    for_all = models.BooleanField(_('для всех'),)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = _('уведомление')
        verbose_name_plural = _('уведомлении')