from django.contrib.admin import register, ModelAdmin

from project.apps.crm.models import AllTime, Location, Age, Section, GroupType, Days, Clients, FormClient, OtherData, \
    CoachForClient, NewClientCoach, ClassAttendance


@register(AllTime)
class AllTimeAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('time',)}),
    )
    list_display = ('id', 'time',)
    model = AllTime


@register(Location)
class LocationAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('location',)}),
    )
    list_display = ('id', 'location',)
    model = Location


@register(Age)
class AgeAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('age',)}),
    )
    list_display = ('id', 'age',)
    model = Age


@register(Section)
class SectionAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('section', 'key')}),
    )

    list_display = ('id', 'section', 'key')
    model = Section


@register(GroupType)
class GroupTypeAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('class_type',)}),
    )
    list_display = ('id', 'class_type',)
    model = GroupType


@register(Days)
class DaysAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('day',)}),
    )
    list_display = ('id', 'day',)
    model = Days


@register(Clients)
class ClientsAdmin(ModelAdmin):
    fieldsets = (
        ('Базовая информация:', {'fields': ('fullname', 'phone_number')}),
        ('Статусы пользователя:',
         {'fields': ('status', 'status_operator', 'status_coach', 'payed_status', 'payed_date')}),
        ('Дата обновление и добавление клиента:', {'fields': ('date_added', 'date_update')}),
    )
    readonly_fields = ('date_added', 'date_update')
    list_display = ('id', 'fullname', 'phone_number', 'status', 'status_coach', 'date_added')
    model = Clients


@register(FormClient)
class FormClientAdmin(ModelAdmin):
    fieldsets = (
        ('Форма клиента:', {'fields': ('client',)}),
        ("Данные формы:", {'fields': ('location', 'visit_time', 'section', 'class_type', 'age', 'visit_day')}),
    )
    list_display = ('id', 'client')
    readonly_fields = ('client',)


@register(OtherData)
class OtherDataAdmin(ModelAdmin):
    fieldsets = (
        ('Форма клиента:', {'fields': ('client',)}),
        ('Данные формы:', {'fields': ('location', 'section')}),
    )
    list_display = ('id', 'client')
    readonly_fields = ('client',)
    model = OtherData


@register(CoachForClient)
class CoachForClientAdmin(ModelAdmin):
    fieldsets = (
        ('Тренер:', {'fields': ('coach',)}),
        ('Клиента:', {'fields': ('client',)}),
        ('Тип и время занятий:', {'fields': ('visit_time', 'visit_day', 'group_type', 'age')}),
    )
    list_display = ('id', 'coach', 'client')
    model = CoachForClient


@register(NewClientCoach)
class NewClientCoachAdmin(ModelAdmin):
    fieldsets = (
        ('Тренер:', {'fields': ('coach',)}),
        ('Клиента (на проверке):', {'fields': ('client',)}),
    )
    list_display = ('id', 'coach', 'client')
    readonly_fields = ('client',)
    model = NewClientCoach


@register(ClassAttendance)
class ClassAttendanceAdmin(ModelAdmin):
    fieldsets = (
        ('Клиент:', {'fields': ('client',)}),
        ('Посещение:', {'fields': ('visit',)}),
        ('Дата посещения:', {'fields': ('date',)}),
    )
    list_display = ('id', 'client', 'visit', 'date')
    model = ClassAttendance
