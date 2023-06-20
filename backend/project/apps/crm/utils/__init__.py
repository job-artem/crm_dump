from project.apps.crm.models import Clients


def check_client(phone_number) -> Clients | bool:
    try:
        return Clients.objects.get(phone_number=phone_number)
    except Clients.DoesNotExist:
        return False