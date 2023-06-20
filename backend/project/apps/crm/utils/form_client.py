from django.db import IntegrityError

from . import check_client
from .coach import create_relationship
from ..models import Clients, FormClient, OtherData, AllTime, Location, Days, Age, GroupType, Section
from ...authorization.models import User


def register_client(data: dict, user: User):
    if not check_client(data['phone_number']):
        Clients.objects.create(
            fullname=data['name'], phone_number=data['phone_number'],
            payed_status=Clients.NEW_CLIENT, status=Clients.NEW,
            status_coach=Clients.NOT_CHECKED, status_operator=Clients.NOT_CHECK
        ).save()
    client = check_client(data['phone_number'])
    data_base: dict = {'client': client}
    data_other: dict = {'client': client}

    if loc := data.get('training_location'):
        data_base['location'] = return_location(loc)
    if loc := data.get('other_location'):
        data_other['location'] = create_location(loc)

    data_base['visit_time'] = return_time_by_id(data['training_time'])

    if sec := data.get('matrial_arts_type') or (sec_2 := data.get('yoga_type')):
        section = sec or sec_2
        data_base['section'] = return_section_by_list(section)
    if sec := data.get('other_matrial_arts_type') or (sec_2 := data.get('other_yoga_type')):
        data_other['section'] = create_section(sec, data['choice']) or create_section(sec_2, data['choice'])

    data_base['age'] = return_age(data['age'])
    data_base['visit_day'] = data['visit_day']
    data_base['class_type'] = return_group_type(data['class_type'])

    dict_filter(data_base, FormClient)
    dict_filter(data_other, OtherData)
    if user.is_anonymous or user.user_type not in ['coach', 'head_coach']:
        return

    create_relationship(
        client=client, coach=user, visit_time=data_base['visit_time'],
        visit_day=data_base['visit_day'],
        group_type=data_base['class_type'], age=data_base['age']
    )
    client.status = Clients.RECORDED
    client.status_operator = Clients.CHECKED_UPLOAD
    client.status_coach = Clients.RECORDED
    client.save()


def return_location(data: list) -> list:
    return [
        element
        for element in Location.objects.filter(id__in=data)
    ]


def return_age(data: int) -> Age:
    return Age.objects.get(id=data)


def return_group_type(data: int) -> GroupType:
    return GroupType.objects.get(id=data)


def create_section(data: str, key: str) -> list:
    key = 'yoga_sec_' if key == 'yoga' else 'mat_sec_'
    try:
        return [Section.objects.get(section=data)]
    except Section.DoesNotExist:
        return sub_create_section(data, key)


def sub_create_section(data: str, key: str) -> list:
    iteration = 1
    while True:
        try:
            section = Section.objects.create(section=data, key=f'{key}{iteration}')
            section.save()
            return [section]
        except IntegrityError:
            iteration += 1


def return_section_by_list(data: list) -> list:
    return [
        element
        for element in Section.objects.filter(key__in=data)
    ]


def return_time_by_id(data: list) -> list:
    return [
        element.id
        for element in AllTime.objects.filter(id__in=data)
    ]


def create_location(data: str) -> list:
    try:
        return [Location.objects.get(location=data)]
    except Location.DoesNotExist:
        location = Location.objects.create(location=data)
        location.save()
        return [location]


def dict_filter(dict_obj: dict, model: FormClient or OtherData) -> None:
    for key, value in dict_obj.items():
        if key == 'clients' or type(value) == Clients or len(value) == 0:
            continue
        return create_form(model, dict_obj)
    return None


def create_form(model: FormClient or OtherData, data: dict):
    if model == FormClient:
        model = model.objects.create(client=data['client'], age=data['age'], class_type=data['class_type'])
        if 'location' in data:
            for location in data['location']:
                model.location.add(location)
        if 'visit_time' in data:
            for visit_time in data['visit_time']:
                model.visit_time.add(visit_time)
        if 'visit_day' in data:
            for visit_day in data['visit_day']:
                model.visit_day.add(visit_day)
        if 'section' in data:
            for section in data['section']:
                model.section.add(section)
        model.save()
    if model == OtherData:
        model = model.objects.create(client=data['client'])
        if 'location' in data:
            for location in data['location']:
                model.location.add(location)
        if 'section' in data:
            for section in data['section']:
                model.section.add(section)
        model.save()


def clean_data(data: dict) -> dict:
    data: dict = data['data']
    delete_key = [key for key, value in data.items() if not value]
    for key in delete_key:
        del data[key]
    return data


def get_form_data() -> dict:
    return dict(
        time=[{"title": element.time, "value": element.id} for element in AllTime.objects.all()],
        location=[{"title": element.location, "value": element.id} for element in Location.objects.all()],
        days=[{"title": element.day, "value": element.id} for element in Days.objects.all()],
        age=[{"title": element.age, "value": element.id} for element in Age.objects.all()],
        groups_type=[{"title": element.class_type, "value": element.id} for element in GroupType.objects.all()],
        **return_section()
    )


def return_section() -> dict:
    all_section = Section.objects.all()
    return dict(
        yoga_type=[{"title": element.section, "value": element.key} for element in all_section if
                   'yoga_sec_' in element.key],
        matrial_arts_type=[{"title": element.section, "value": element.key} for element in all_section if
                           'mat_sec_' in element.key],
    )
