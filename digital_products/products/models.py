import random

from django.utils import timezone
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail, UserManager


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

    def __str__(self):
        return self.title



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username = username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined = now, **extra_fields)

        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user


    def create_user(self, username=None, phone_number=None, email=None, passwrod=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]

            while User.objects.filter(username=username).exists():
                username += str(random.randint(10,99))

        return self._create_user(username, phone_number, email, passwrod, False, False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number' : phone_number})




class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=32, unique=True,
                                    help_text = _(
                                        'Required. 30 characters or fewer starting with a letter. Letters, digital'
                                    ),
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$' ,
                                                              _('Enter a valid username starting with a-z.'))
                                ],
                                error_messages={
                                    'unique' : _("A user with that username already exists.")
                                })

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(_('mobile number'), unique=True, null=True, blank=True,
                                          validators={
                                              validators.RegexValidator(r'^989[0-3]\d{8}$',
                                                                        ("Enter a valid mobile number,"),)
                                          },
                                          error_messages={
                                              'unique': _("A user with this mobile number already exists.")
                                          })
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designates whether the user can log into this admin site"))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_("Designates whether this user should be treated as active."
                                                'Unselect this instead of deleting account.'))
    data_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen data'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _("user")
        verbose_name_plural = _('users')


    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):

        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'), max_length=150, blank=True)
    profile_photo = models.ImageField(_('profile_image'), blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.NullBooleanField(_('gender'), help_text=_('female is False, male is True, null is unset'))
    province = models.ForeignKey(verbose_name=_('province'), to='Province', on_delete=models.SET_NULL)

    class Meta:
        db_table = 'user_profiles'
        verbose_name= _('profile')
        verbose_name_plural = _('profiles')

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nickname(self):
        return self.nick_name if self.nick_name else self.user.username


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android')
    )

    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True)

    last_login = models.DateTimeField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(_('device model'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'user_devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together= ("user", 'device_uuid')




# Create your models here.
