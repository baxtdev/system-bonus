from unicodedata import category
from django.db import models
from django.forms import Textarea
from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField
from accounts.models import User


class Categories(models.Model):
    def __str__(self):
        return self.title

    class Meta:
        db_table = "categories"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    title = models.CharField(max_length=200, verbose_name="Названия")
    description = models.TextField(verbose_name="Описание")


class News(models.Model):
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    title = models.CharField(max_length=200, verbose_name="Названия")
    image = ImageField(upload_to='images', blank=True, verbose_name="Изображение")
    description = RichTextField(verbose_name="Описание")
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    edited_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)
    published = models.BooleanField(default=True, verbose_name="Опубликовано")
    slug = models.SlugField(verbose_name="Ярлык", unique=True)

    category = models.ForeignKey(Categories, verbose_name="Категория", related_name='news',on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_news')
    seo_title = models.CharField(max_length=200, verbose_name="SEO Title", blank=True)
    seo_description = models.CharField(max_length=300, verbose_name="SEO Description", blank=True)

    def get_absolute_url(self):
        return '%s-%s' % (self.slug, self.pk)