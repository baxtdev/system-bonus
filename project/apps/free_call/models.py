from django.db import models

class FreeCall(models.Model):
    def __str__(self):
        return self.theme

    class Meta:
        db_table = "free_call"
        verbose_name = 'Заявка на звонок'
        verbose_name_plural = 'Заявки на звонок'

    name = models.CharField(max_length=100, verbose_name='Имя')
    theme = models.CharField(max_length=50, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообшения", blank=True)
    status = models.BooleanField(verbose_name="Обработана?", default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")
