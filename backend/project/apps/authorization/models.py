from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db.models import (
    Model, EmailField, BooleanField, DateTimeField, CharField, ForeignKey,
    DO_NOTHING, CASCADE
)
from django.forms import model_to_dict
from django_resized import ResizedImageField

from project.apps.authorization import path_to_image_profile


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields) -> User:
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if user.is_superuser and user.is_staff:
            user.is_active = True
            user.email_verify = True
            user.user_type = User.ADMIN
            user.user_group = User.EMPTY
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields) -> User:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields) -> User:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    ADMIN = 'admin'
    USER = 'user'
    COACH = 'coach'
    HEAD_COACH = 'head_coach'
    OPERATOR = 'operator'

    USER_STATUS = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (COACH, 'Тренер'),
        (HEAD_COACH, 'Старший тренер'),
        (OPERATOR, 'Оператор'),
    )

    EMPTY = 'empty'
    YOGA = 'yoga'
    MARTIALARTS = 'martialarts'
    COACH_SECTION = (
        (EMPTY, 'Отсутствует'),
        (YOGA, 'Тренер йоги'),
        (MARTIALARTS, "Тренер единоборств"),
    )

    email = EmailField(verbose_name='Електронная почта', db_index=True, unique=True)
    email_verify = BooleanField(default=False)
    is_active = BooleanField(default=False, verbose_name='Активный')

    user_type = CharField(
        verbose_name="Тип профиля", choices=USER_STATUS,
        default=USER, max_length=20
    )

    user_group = CharField(
        verbose_name='Секция тренера', max_length=255, choices=COACH_SECTION,
        default=EMPTY, blank=True, null=True
    )

    image = ResizedImageField(
        verbose_name='Изображение профиля', force_format="WEBP", quality=100,
        upload_to=path_to_image_profile, blank=True, null=True
    )
    phone_number = CharField(
        verbose_name='Номер телефона', blank=True,
        null=True, max_length=255
    )

    create_at = DateTimeField(verbose_name="Дата регистрации", auto_now_add=True, editable=False, )
    update_at = DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.email} {self.first_name} {self.last_name}'

    def generate_confirmation_token(self) -> str:
        token = EmailActivateToken.objects.create(
            user=self, confirmation_token=token_urlsafe())
        token.save()
        return token.confirmation_token

    @staticmethod
    def get_by_confirmation_token(token) -> User or None:
        try:
            return EmailActivateToken.objects.get(
                confirmation_token=token).user
        except EmailActivateToken.DoesNotExist:
            return None

    def confirm_registration(self, token) -> None:
        self.email_verify = True
        self.is_active = True
        EmailActivateToken.objects.get(confirmation_token=token).delete()
        self.save()


class EmailActivateToken(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    confirmation_token = CharField(
        verbose_name='Токен', null=True, blank=True, max_length=255)


class TypeSection(Model):
    section_type = CharField(verbose_name='Направление секции', max_length=255)


class SectionYoga(Model):
    yoga = ()
    type_section = ForeignKey(TypeSection, verbose_name='Направление', on_delete=DO_NOTHING)
    sub_type_section = CharField(verbose_name='Тип секции', max_length=255)


class SectionFighter(Model):
    fighter = ()
    type_section = ForeignKey(TypeSection, verbose_name='Направление', on_delete=DO_NOTHING)
    sub_type_section = CharField(verbose_name='Тип секции', max_length=255)
