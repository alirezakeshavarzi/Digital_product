from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(blank=True, upload_to='categories')
    is_enable = models.BooleanField(_('is enable'), default=True, )
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        db_table = 'categories' # A table that create in databases.
        verbose_name='Category' # Show this name in admin panel.
        verbose_name_plural = 'Categories' # برای اسم جمع

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(blank=True, upload_to='products/')
    is_enable = models.BooleanField(_('is enable'), default=True, )
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        db_table = 'products' # A table that create in databases.
        verbose_name= _('products') # Show this name in admin panel.
        verbose_name_plural = _('products') # برای اسم جمع



class File(models.Model):
    product = models.ForeignKey('Product', verbose_name=_('product'), on_delete=models.CASCADE, null=True)
    title = models.CharField(_('title'), max_length=50)
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(_('is enable'), default=True, )
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    create_time = models.DateTimeField(_('create time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name=_('file')
        verbose_name_plural = _('files')
# Create your models here.
