from functools import total_ordering
from django.db import models
from django.utils.translation import gettext_lazy as _


from accounts.models import Notification, User

# Pharmacy App Models

class Pharmacy(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    address = models.CharField(max_length=100, verbose_name=_('Адрес'))
    phone = models.CharField(max_length=100, verbose_name=_('Телефон'))
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Электронная почта'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Аптека')
        verbose_name_plural = _('Аптеки')


class Manager(models.Model):
    """
    Manager model
    """
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Менеджер'),related_name='manager')
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, verbose_name=_('Аптека'))
    contact = models.CharField(max_length = 10, blank=True, verbose_name=_('Контакт'))
    email = User.email

    def __str__(self):
        return self.manager.first_name + " " + self.manager.last_name + " - " + str(self.contact)

    class Meta:
        verbose_name = _('Менеджер')
        verbose_name_plural = _('Менеджеры')


METHODS = (
    (0, "Добавить"),
    (1, "Снять"),
)


class History(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Покупатель'))
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name=_('Менеджер'))
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, verbose_name=_('Аптека'))
    method = models.IntegerField(choices=METHODS, default=None)
    bonus = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name + " - " + str(self.method)

    @property
    def customer_bonus(self):
        return self.customer.bonus
    customer_bonus.fget.short_description = "Customer bonus"

    class Meta:
        db_table = "history"
        verbose_name = _('История')
        verbose_name_plural = _('Истории')

    def save(self, *args, **kwargs):
        Notification.objects.create(
                    name =f'{METHODS[self.method][1]}',
                    image = None,
                    content = f'-{self.bonus}, текущий баланс :{self.customer_bonus}, дата :{self.date} аптека :{self.pharmacy}, продавец :{self.manager}',
                    user = self.customer,
                    for_all = False
                )    
        super().save(*args, **kwargs)



# Товары по скидке
class DiscountItems(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    price = models.IntegerField(verbose_name=_('Цена оригинала'))
    discount = models.IntegerField(verbose_name=_('Цена со скидкой'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))
    image = models.ImageField(upload_to='discount_items', blank=True, null=True, verbose_name=_('Изображение'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Товар по скидке')
        verbose_name_plural = _('Товары по скидке')