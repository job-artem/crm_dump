from datetime import datetime

from django.db.models import QuerySet
from django.utils import timezone

from . import check_client
from .operators import return_client_data
from ..models import (
    CoachForClient, Clients, ClassAttendance,
    NewClientCoach, AllTime, GroupType, Days,
    Age, Section, Location, FormClient
)
from ...authorization.models import User


def get_clients_for_coach(user: User) -> list:
    clients = CoachForClient.objects.filter(coach=user)
    client: CoachForClient
    return [{'id': client.client.id, 'fullname': client.client.fullname, 'phone_number': client.client.phone_number,
             'payed_status': change_status(client.client.payed_status),
             'status': change_status(client.client.payed_status), 'exist': get_visit(client.client)} for client in
            clients]


def change_status(status: str) -> str:
    return [elements[1] for element in Clients.PAID_STATUS if status in (elements := list(element))][0]


def get_status_paid() -> list:
    return [list(element)[1] for element in Clients.PAID_STATUS]


def clear_data(data: dict) -> dict:
    element: dict
    field = ['exist', 'status']
    for element in data['clients']:
        for keys in field:
            if keys not in element:
                element[keys] = False
    return data


def mark_visit_creation(data: dict, coach: User) -> None:
    client: dict
    time_correct = timezone.now().date()
    clients = [check_create_client(client, coach, time_correct) for client in data['clients']]
    [create_visit(visit=data['exist'], client=data['client']) for data in clients]


def check_create_client(client: dict, coach: User, time_correct: datetime) -> dict:
    if not (correct_client := check_client(client['phone_number'])):
        correct_client = Clients.objects.create(
            fullname=client['fullname'], phone_number=client['phone_number'],
            payed_status=return_payed_status(client['status']), status_operator=Clients.CHECKED_UPLOAD,
            status_coach=Clients.CHECKED_UPLOAD
        )
        if correct_client.payed_status == 'paid':
            correct_client.payed_date = f'{time_correct.year}-{time_correct.month}-{time_correct.day}'
        create_relationship(
            coach=coach, client=correct_client,
            visit_time=client['visit_time'], visit_day=client['visit_day'],
            group_type=client['class_type'], age=client['age']
        )
        correct_client.status = correct_client.RECORDED
    correct_client.fullname = client['fullname']
    correct_client.payed_status = return_payed_status(client['status'])
    if correct_client.payed_status == 'paid':
        correct_client.payed_date = f'{time_correct.year}-{time_correct.month}-{time_correct.day}'
    correct_client.save()
    return dict(client=correct_client, exist=client['exist'])


def get_visit(client: Clients) -> bool:
    try:
        exist = ClassAttendance.objects.get(client=client, date=datetime.now().date())
        return exist.visit
    except ClassAttendance.DoesNotExist:
        return False


def create_visit(visit: bool, client: Clients):
    date_now = datetime.now().date()
    try:
        element = ClassAttendance.objects.get(date=date_now, client=client)
        element.visit = visit
        element.save()
    except ClassAttendance.DoesNotExist:
        ClassAttendance.objects.create(visit=visit, client=client).save()


def return_payed_status(data: str) -> str:
    status = [elements[0] for element in Clients.PAID_STATUS if data in (elements := list(element))][0]
    return Clients.NOTPAID if not status else status


def create_relationship(
        coach: User, client: Clients,
        visit_time: list, group_type: int,
        visit_day: list, age: int
) -> None:
    try:
        model = CoachForClient.objects.get(
            coach=coach, client=client,
            group_type=group_type,
            age=age
        )
    except CoachForClient.DoesNotExist:
        model = CoachForClient.objects.create(
            coach=coach, client=client,
            group_type=group_type,
            age=age
        )
        model.save()
    if visit_time:
        for visit_times in return_time_by_id(visit_time):
            model.visit_time.add(visit_times)
    if visit_day:
        for visit_days in return_day_by_id(visit_day):
            model.visit_day.add(visit_days)
    model.save()


def return_group_type_by_id(data: int) -> GroupType:
    return GroupType.objects.get(id=data)


def return_age_by_id(data: int) -> Age:
    return Age.objects.get(id=data)


def return_time_by_id(data: list) -> list:
    return [element for element in AllTime.objects.filter(id__in=data)]


def return_day_by_id(data: list) -> list:
    return [element for element in Days.objects.filter(id__in=data)]


def new_clients(coach: User) -> list:
    return change_choose_data(recreate_client_data(return_clients_list(return_clients(coach))))


def change_choose_data(data: list) -> list:
    element: dict
    for element in data:
        element['visit_day'] = recreate_date(element['visit_day'])
        element['visit_time'] = recreate_date(element['visit_time'])
        element['location'] = recreate_date(element['location'])
        element['section'] = recreate_date(element['section'])
        element['class_type'] = [{'title': 'Персональные', 'value': 'single'},
                                 {'title': 'Групповые', 'value': 'group'}]

    return data


def recreate_date(data: list) -> list:
    if type(data) == str:
        return [dict(
            title=data,
            value=data
        )]
    return [dict(
        title=element,
        value=element
    ) for element in data]


def return_clients(coach: User) -> QuerySet:
    return NewClientCoach.objects.filter(coach=coach)


def return_clients_list(data: QuerySet) -> list:
    element: NewClientCoach
    return [element.client for element in data]


def recreate_client_data(data: list) -> list:
    element: Clients
    return [dict(
        id=element.id,
        fullname=element.fullname,
        phone_number=element.phone_number,
        **return_client_data(element),
        status=return_coach_status(element.status_coach)
    ) for element in data]


def return_coach_status(status: str) -> str:
    return [elements[0] for element in Clients.COACH_STATUS if status in (elements := list(element))][0]


def create_new_clients_coach(data: dict, coach: User):
    data = convert_data(cleared_data(data))
    if not data:
        return
    for element in data['clients']:
        client: Clients = element['client']
        client.fullname = element['name']
        client.payed_status = Clients.NEW_CLIENT
        client.status_coach = element['status']
        client.save()
        delete_temporary_coach_client(coach=coach, client=client)
        if client.status_coach == Clients.NOT_RECORDED:
            continue
        for detail in FormClient.objects.filter(client=client):
            create_relationship(
                coach=coach, client=client,
                visit_time=[element.id for element in detail.visit_time.all()],
                visit_day=[element.id for element in detail.visit_day.all()],
                group_type=detail.class_type, age=detail.age
            )


def delete_temporary_coach_client(coach: User, client: Clients):
    try:
        NewClientCoach.objects.get(coach=coach, client=client).delete()
    except NewClientCoach.DoesNotExist:
        pass


def convert_data(data: dict) -> dict:
    print(data)
    return {'clients': [
        {'client': Clients.objects.get(id=element['id']), 'status': element['status'], 'name': element['fullname']}
        for element in data['clients']]}


def convert_details(data: list, age: str) -> list:
    return [dict(
        class_type=convert_class_type(element['class_type']),
        section=convert_section(element['section']),
        visit_time=convert_time(element['visit_time']),
        visit_day=convert_day(element['visit_day']),
        location=convert_location(element['location']),
        age=convert_age(age),
    ) for element in data]


def convert_class_type(data: str) -> int:
    return GroupType.objects.get(class_type=data).id


def convert_section(data: str) -> list:
    return [Section.objects.get(section=data).id]


def convert_time(data: str) -> list:
    return [AllTime.objects.get(time=data).id]


def convert_day(data: str) -> list:
    return [Days.objects.get(day=data).id]


def convert_age(data: str) -> int:
    return Age.objects.get(age=data).id


def convert_location(data: str) -> Location:
    return Location.objects.get(location=data)


def cleared_data(data: dict) -> dict:
    return {'clients': [
        {'id': element['id'], 'status': element['status'], 'fullname': element['fullname']}
        for element in data['clients']
        if element['status'] != Clients.NOT_CHECKED
    ]}


def return_time() -> list:
    time: AllTime
    return [
        dict(
            title=time.time,
            value=time.id
        ) for time in AllTime.objects.all()
    ]


def return_day() -> list:
    time: Days
    return [
        dict(
            title=time.day,
            value=time.id
        ) for time in Days.objects.all()
    ]


def return_age() -> list:
    time: Age
    return [
        dict(
            title=time.age,
            value=time.id
        ) for time in Age.objects.all()
    ]


def return_class_type() -> list:
    class_type: GroupType
    return [
        dict(
            title=class_type.class_type,
            value=class_type.id
        ) for class_type in GroupType.objects.all()
    ]
