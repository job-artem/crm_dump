from django.db.models import QuerySet
from django.forms import model_to_dict

from ..models import Clients, FormClient, OtherData, GroupType, NewClientCoach, CoachForClient, Age
from ...authorization.models import User


def get_all_new_clients() -> list:
    all_clients = Clients.objects.filter(status=Clients.NEW)
    return recreate_client_data(all_clients)


def recreate_client_data(data: QuerySet) -> list:
    element: Clients
    return [
        dict(
            id=element.id,
            fullname=element.fullname,
            **return_client_data(element),
            phone_number=element.phone_number,
            date_added=element.date_added,
            date_update=element.date_update,
            crm_status=return_crm_status(element.status_operator),
            data=element.date_added,
            coach=return_coach(element)
        )
        for element in data
    ]


def return_crm_status(data: str) -> list:
    return [element[1] for elements in Clients.CRM_STATUS if data in (element := list(elements))][0]


def return_coach(data: Clients) -> list | bool:
    element: CoachForClient or NewClientCoach
    coach = [f"{element.coach.last_name} {element.coach.first_name}" for element in
             CoachForClient.objects.filter(client=data)]
    if len(coach) == 0:
        coach = [f"{element.coach.last_name} {element.coach.first_name}" for element in
                 NewClientCoach.objects.filter(client=data)]
    return coach if len(coach) > 0 else 0


def get_operator_client_status() -> list:
    return [
        dict(
            label=list(element)[1],
            value=list(element)[0]
        ) for element in Clients.CRM_STATUS
    ]


def get_all_coach() -> list:
    element: User
    return [
        dict(
            label=f'{element.last_name} {element.first_name}',
            value=element.id
        ) for element in User.objects.filter(user_type__in=[User.COACH, User.HEAD_COACH])
    ] + [dict(
        label='Не выбран',
        value=0
    )]


def get_group_client_status() -> list:
    return [
        dict(
            label=element.class_type,
            value=element.id
        ) for element in GroupType.objects.all()
    ]


def return_client_data(element: Clients) -> dict:
    data = return_data(element)
    if data.get('form_data') and data.get('other_data'):
        return return_base_and_other_data(data)
    elif not data.get('form_data') and data.get('other_data'):
        return return_some_data(data, 'other_data')
    elif data.get('form_data') and not data.get('other_data'):
        return return_some_data(data, 'form_data')
    if not data:
        return return_data_by_coach(element)


def return_base_and_other_data(data: dict) -> dict:
    data_returned = dict()
    data_returned['location'] = [element.location for element in data['form_data']['location']]
    data_returned['location'] += [element.location for element in data['other_data']['location']]
    data_returned['section'] = [element.section for element in data['form_data']['section']]
    data_returned['section'] += [element.section for element in data['other_data']['section']]
    data_returned['visit_time'] = [element.time for element in data['form_data']['visit_time']]
    data_returned['visit_day'] = [element.day for element in data['form_data']['visit_day']]
    data_returned['class_type'] = return_class_type(data['form_data']['class_type'])
    data_returned['age'] = return_age(data['form_data']['age'])
    del data['form_data']['location']
    del data['form_data']['section']
    del data['form_data']['visit_time']
    del data['form_data']['visit_day']
    del data['form_data']['class_type']
    del data['form_data']['age']
    del data['other_data']['location']
    del data['other_data']['section']
    del data['form_data']['id']
    del data['other_data']['id']
    return {**data_returned, **data['form_data'], **data['other_data']}


def return_some_data(data: dict, key: str) -> dict:
    data_returned = dict()
    data_returned['location'] = [element.location for element in data[key]['location']]
    data_returned['section'] = [element.section for element in data[key]['section']]
    data_returned['visit_time'] = [element.time for element in data[key]['visit_time']]
    data_returned['visit_day'] = [element.day for element in data[key]['visit_day']]
    data_returned['class_type'] = return_class_type(data[key]['class_type'])
    data_returned['age'] = return_age(data[key]['age'])
    del data[key]['location']
    del data[key]['section']
    del data[key]['visit_time']
    del data[key]['visit_day']
    del data[key]['age']
    del data[key]['class_type']
    del data[key]['id']

    return {**data_returned, **data[key]}


def return_data_by_coach(client: Clients) -> dict:
    data: CoachForClient = CoachForClient.objects.get(client=client)
    return dict(
        section=None,
        location=None,
        visit_time=', '.join([element.time for element in data.visit_time.all()]),
        visit_day=', '.join([element.day for element in data.visit_day.all()]),
        class_type=data.group_type.class_type,
        age=data.age.age
    )


def return_age(data: int) -> str:
    return Age.objects.get(id=data).age


def return_class_type(data: int) -> str:
    return GroupType.objects.get(id=data).class_type


def return_data(element: Clients) -> dict:
    data = {}
    try:
        form_data = model_to_dict(FormClient.objects.filter(client=element)[0])
        del form_data['client']
        data["form_data"] = form_data
    except (FormClient.DoesNotExist, IndexError):
        pass
    try:
        other_data = model_to_dict(OtherData.objects.filter(client=element)[0])
        del other_data['client']
        data["other_data"] = other_data
    except (OtherData.DoesNotExist, IndexError):
        pass
    return data


def add_clients_to_coach(data: dict) -> None:
    clients = data['clients']
    client: dict
    for client in clients:
        client['crm_status'] = [el[0] for elem in Clients.CRM_STATUS if client['crm_status'] in (el := list(elem))][0]
        if not client['coach'] or client['crm_status'] == Clients.NOT_CHECK:
            continue
        client_object = Clients.objects.get(id=client['id'])
        client_object.status_operator = client['crm_status']
        if client_object.status_operator == Clients.CHECKED_CLOSED:
            client_object.status = Clients.REFUSAL
            client_object.save()
            continue
        client_object.status = Clients.RECORDED
        client_object.status_coach = Clients.NOT_CHECKED
        client_object.save()
        create_temporary_relationship(client_object, client['coach'])


def create_temporary_relationship(client: Clients, coach: id) -> None:
    NewClientCoach.objects.create(
        client=client,
        coach=User.objects.get(id=coach)
    ).save()


def get_all_clients() -> list:
    return recreate_client_data(get_all_clients_coach())


def get_all_clients_coach() -> QuerySet:
    return Clients.objects.all().exclude(status=Clients.NEW)
