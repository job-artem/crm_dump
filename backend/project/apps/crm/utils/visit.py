from datetime import timedelta

from django.utils.timezone import now

from project.apps.authorization.models import User
from project.apps.crm.models import CoachForClient, ClassAttendance, Clients


def return_data_visit(user: User, data: dict) -> dict:
    date = return_date_period_by_str(data['date'])
    clients = return_clients(user)
    attention = return_attentions(clients, date)
    header = create_header(date)
    return {
        'header': header,
        'attention': attention
    }


def create_header(date: dict) -> list:
    headers = [
        {'title': 'Клиент', 'key': 'client'},
        {'title': 'Номер телефона', 'key': 'client_number'},
    ]
    start_date = date['start']
    end_date = date['end']
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        headers.append({'title': date_str, 'key': 'date_' + date_str})
        current_date += timedelta(days=1)
    return headers

def return_clients(user: User) -> list:
    return [data.client for data in CoachForClient.objects.filter(coach=user)]


def return_attentions(clients: list, date: dict) -> list:
    attentions = {}
    for data in ClassAttendance.objects.filter(
            client__in=clients, date__gte=date['start'], date__lte=date['end']
    ):
        attention = {
            'client': data.client.fullname,
            'client_number': data.client.phone_number,
            **sub_date_work(date, data.client),
        }
        attentions[data.client.fullname] = attention

    return [{**value} for key, value in attentions.items()]


def sub_date_work(date: dict, client: Clients) -> dict:
    base_date = {}
    start_date = date['start']
    end_date = date['end']
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        base_date['date_' + date_str] = ''
        current_date += timedelta(days=1)
    attendance_data = ClassAttendance.objects.filter(
        client=client, date__gte=date['start'], date__lte=date['end']
    )
    for data in attendance_data:
        date_str = data.date.strftime('%Y-%m-%d')
        base_date['date_' + date_str] = 'Отсутствовал' if not data.visit else 'Присутствовал'

    return base_date




def return_date_period_by_str(date: str) -> dict:
    date_today = now().date()
    match date:
        case "Сегодня":
            return {
                'start': date_today,
                'end': date_today + timedelta(days=1)
            }
        case "Неделя":
            return {
                'start': date_today - timedelta(days=7),
                'end': date_today + timedelta(days=1)
            }
        case "3 месяца":
            return {
                'start': date_today - timedelta(days=30),
                'end': date_today + timedelta(days=1)
            }
        case "Полгода":
            return {
                'start': date_today - timedelta(days=180),
                'end': date_today + timedelta(days=1)
            }
        case "Год":
            return {
                'start': date_today - timedelta(days=365),
                'end': date_today + timedelta(days=1)
            }
