from django.db.models import (
    DO_NOTHING, ForeignKey, Model, CharField,
    DateTimeField, DateField, BooleanField, CASCADE,
    ManyToManyField
)

from ..authorization.models import User


class AllTime(Model):
    time = CharField(verbose_name='Рабочее время', max_length=20, db_index=True)

    class Meta:
        verbose_name = 'Рабочее время'
        verbose_name_plural = 'Рабочие времена'

    def __str__(self):
        return self.time


class Clients(Model):
    PAID = 'paid'
    NOTPAID = 'notpaid'
    PAUSE = 'pause'
    FIRST = 'first'
    PART = 'part'
    ONE_PAID = 'one_paid'
    THIS_MONTH = 'this_month'
    NEW_CLIENT = 'new_client'
    PAID_STATUS = (
        (PAID, 'Оплачен'),
        (NOTPAID, 'Не оплачен'),
        (PAUSE, 'Пауза'),
        (FIRST, 'Первая тренировка'),
        (PART, 'Частичная оплата'),
        (ONE_PAID, 'Поразово'),
        (THIS_MONTH, 'Долг свыше месяца'),
        (NEW_CLIENT, 'Новый клиент')
    )

    NEW = 'new'
    RECORDED = 'recorded'
    REFUSAL = 'refusal'
    CLIENT_STATUS = (
        (NEW, 'Новый клиент'),
        (REFUSAL, 'Отказ'),
        (RECORDED, 'Записан'),
    )

    NOT_CHECK = 'not_check'
    CHECKED_UPLOAD = 'checked_upload'
    CHECKED_CLOSED = 'checked_closed'
    CRM_STATUS = (
        (NOT_CHECK, 'Не проверен'),
        (CHECKED_UPLOAD, 'Проверен, записан'),
        (CHECKED_CLOSED, 'Проверен, отказ'),
    )

    NOT_CHECKED = 'not_checked'
    RECORDED = 'recorded'
    NOT_RECORDED = 'not_recorded'
    COACH_STATUS = (
        (RECORDED, 'Записан'),
        (NOT_CHECKED, 'Не проверен'),
        (NOT_RECORDED, 'Отказ'),
    )

    status = CharField(verbose_name='Статус клиента', choices=CLIENT_STATUS, default=NEW, max_length=255)
    status_operator = CharField(verbose_name='Статус оператора', choices=CRM_STATUS, default=NOT_CHECK,
                                max_length=255)
    status_coach = CharField(verbose_name='Статус проверки тренера', choices=COACH_STATUS, default=NOT_CHECKED,
                             max_length=255)
    payed_status = CharField(choices=PAID_STATUS, default=NOTPAID, verbose_name='Статус оплаты', max_length=255)
    fullname = CharField(verbose_name='Фамилия Имя', max_length=100, blank=True, null=True)
    phone_number = CharField(verbose_name='Номер телефона', max_length=100, unique=True)
    date_added = DateTimeField(auto_now_add=True, verbose_name='Дата добавления клиента')
    date_update = DateTimeField(auto_now=True, verbose_name='Дата обновления данных')
    payed_date = DateField(verbose_name='Дата оплаты', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.fullname} - {self.phone_number}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClassAttendance(Model):
    visit = BooleanField(default=False, verbose_name='Посещение')
    client = ForeignKey(Clients, on_delete=CASCADE, verbose_name='Клиент')
    date = DateField(auto_now=True, verbose_name='Дата посещения')

    def __str__(self) -> str:
        return f"{self.client} - {self.date}"

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'


class Location(Model):
    location = CharField(verbose_name='Место тренировки', max_length=255)

    def __str__(self) -> str:
        return self.location

    class Meta:
        verbose_name = 'Место тренировки'
        verbose_name_plural = 'Места тренировки'


class Age(Model):
    age = CharField(verbose_name='Возрастная группа', max_length=255)

    def __str__(self) -> str:
        return self.age

    class Meta:
        verbose_name = 'Возрастная группа'
        verbose_name_plural = 'Возрастные группы'


class Section(Model):
    section = CharField(verbose_name='Тип секции', max_length=255, unique=True, db_index=True)
    key = CharField(verbose_name='Значение',
                    help_text='В случае добавления новой секции необходимо соблюдать формат ключей, для Йоги - "yoga_sec_ЧИСЛО", для Единоборств - "mat_sec_ЧИСЛО"',
                    max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.section

    class Meta:
        verbose_name = 'Тип секции'
        verbose_name_plural = 'Типы секций'


class GroupType(Model):
    class_type = CharField(verbose_name='Название группы', max_length=255)

    def __str__(self) -> str:
        return self.class_type

    class Meta:
        verbose_name = 'Тип группы'
        verbose_name_plural = 'Типы групп'


class Days(Model):
    day = CharField(verbose_name='День', max_length=255)

    def __str__(self) -> str:
        return self.day

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'


class FormClient(Model):
    location = ManyToManyField(Location, verbose_name='Локации которые были выбраны(ID)', blank=True)
    visit_time = ManyToManyField(AllTime, verbose_name='Время которое было выбрано(ID)', blank=True)
    section = ManyToManyField(Section, verbose_name='Секции которые были выбраны(ID)', blank=True)
    client = ForeignKey(Clients, on_delete=CASCADE, verbose_name='Клиент')
    age = ForeignKey(Age, verbose_name='Возрастная категория(ID)', on_delete=CASCADE)
    visit_day = ManyToManyField(Days, verbose_name='Дни которые были выбраны(ID)')
    class_type = ForeignKey(GroupType, verbose_name='Тип занятий(ID)', on_delete=CASCADE)

    def __str__(self) -> str:
        return f"Базовая форма для - {self.client.fullname} - {self.client.phone_number}"

    class Meta:
        verbose_name = 'Форма клиента'
        verbose_name_plural = 'Формы клиентов'


class OtherData(Model):
    client = ForeignKey(Clients, on_delete=CASCADE, verbose_name='Клиент')
    location = ManyToManyField(Location, verbose_name='Локации которые были выбраны(TEXT)', blank=True)
    section = ManyToManyField(Section, verbose_name='Секции которое были выбраны(TEXT)', blank=True)

    def __str__(self) -> str:
        return f"Форма с нестандартными данными для - {self.client.fullname} - {self.client.phone_number}"

    class Meta:
        verbose_name = 'Форма с нестандартными данными'
        verbose_name_plural = 'Формы с нестандартными данными'


class CoachForClient(Model):
    coach = ForeignKey(User, verbose_name='Тренер', on_delete=DO_NOTHING)
    visit_time = ManyToManyField(AllTime, verbose_name='Время посещения тренировки с тренером')
    visit_day = ManyToManyField(Days, verbose_name='Дни посещения тренировки с тренером')
    age = ForeignKey(Age, verbose_name='Возрастная категория', on_delete=CASCADE)
    group_type = ForeignKey(GroupType, verbose_name='Тип тренировки', on_delete=CASCADE)
    client = ForeignKey(Clients, verbose_name='Клиент', on_delete=CASCADE)

    def __str__(self):
        return f"Тренер - {self.coach.first_name} / Клиент {self.client.fullname}"

    class Meta:
        verbose_name = 'Тренер/Клиент'
        verbose_name_plural = 'Тренеры/Клиенты'


class NewClientCoach(Model):
    coach = ForeignKey(User, verbose_name='Тренер', on_delete=DO_NOTHING)
    client = ForeignKey(Clients, verbose_name='Клиент', on_delete=CASCADE)

    def __str__(self):
        return f"Тренер - {self.coach.first_name} / Клиент {self.client.fullname}"

    class Meta:
        verbose_name = 'Тренер/Клиент (Временная таблица)'
        verbose_name_plural = 'Тренеры/Клиенты (Временная таблица)'
