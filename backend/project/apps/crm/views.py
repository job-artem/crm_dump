from django.http import JsonResponse
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from .permissions import HeightRank, AdminOperator
from .serializers import (
    ClientsSerializer, FormSerializer,
    OperatorCrmClientsSerializer
)
from .utils.coach import (
    get_clients_for_coach, get_status_paid,
    clear_data, mark_visit_creation,
    return_time, new_clients, create_new_clients_coach,
    return_class_type, return_day, return_age
)
from .utils.form_client import register_client, clean_data, get_form_data
from .utils.operators import (
    get_all_new_clients, get_operator_client_status,
    get_group_client_status, get_all_coach,
    add_clients_to_coach, get_all_clients
)
from .utils.visit import return_data_visit


class HealsCheckAPI(RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data={'heals': True}, status=HTTP_200_OK)


class CoachClients(RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = (HeightRank,)
    serializer_class = [ClientsSerializer]

    def serializers_data(self, data: dict) -> dict or bool:
        for serializer in self.serializer_class:
            serializer_data = serializer(data=data)
            if serializer_data.is_valid():
                return {**serializer_data.validated_data}
        return False

    def get(self, request, *args, **kwargs) -> JsonResponse:
        data = get_clients_for_coach(request.user)
        status = get_status_paid()
        work_time = return_time()
        class_type = return_class_type()
        visit_day = return_day()
        ages = return_age()
        return JsonResponse(
            data=dict(
                clients=data, status_paid=status, time=work_time,
                class_type=class_type, visit_day=visit_day,
                ages=ages
            ),
            status=HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        mark_visit_creation(clear_data(self.serializers_data(request.data)), request.user)
        return JsonResponse(data={}, status=HTTP_200_OK)


class NewClientsCoach(CreateAPIView, RetrieveAPIView):
    permission_classes = (HeightRank,)
    serializer_class = [OperatorCrmClientsSerializer]

    def get_data(self, data: dict) -> dict | bool:
        for serializer in self.serializer_class:
            serialize_data = serializer(data=data)
            if serialize_data.is_valid():
                return {**serialize_data.validated_data}
        return False

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data={'elements': new_clients(request.user)}, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        data = self.get_data({'clients': request.data['data']})
        create_new_clients_coach(data, request.user)
        return JsonResponse(data={}, status=HTTP_200_OK)


class NewClientsWithFormsAPI(CreateAPIView, RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = [FormSerializer]

    def serializer_data(self, data: dict) -> dict | bool:
        for serializer in self.serializer_class:
            new_data = serializer(data=data)
            if new_data.is_valid():
                return {**new_data.validated_data}
        return False

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data=get_form_data(), status=HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        register_client(self.serializer_data(clean_data(request.data)), request.user)
        return JsonResponse(data={}, status=HTTP_200_OK)


class AdminAndOperatorForm(CreateAPIView, RetrieveAPIView):
    permission_classes = [AdminOperator]
    serializer_class = [OperatorCrmClientsSerializer]

    def get_data(self, data: dict) -> dict | bool:
        for serializer in self.serializer_class:
            serialize_data = serializer(data=data)
            if serialize_data.is_valid():
                return {**serialize_data.validated_data}
        return False

    def post(self, request, *args, **kwargs) -> JsonResponse:
        add_clients_to_coach(self.get_data(request.data))
        return JsonResponse(data={}, status=HTTP_200_OK)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
            data={
                'elements': get_all_new_clients(), 'crm_status': get_operator_client_status(),
                'group_type': get_group_client_status(), 'coach': get_all_coach()
            },
            status=HTTP_200_OK
        )


class AllClients(RetrieveAPIView):
    permission_classes = [AdminOperator]

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
            data={
                'elements': get_all_clients(), 'crm_status': get_operator_client_status(),
                'group_type': get_group_client_status(), 'coach': get_all_coach()
            },
            status=HTTP_200_OK
        )


class VisitTable(RetrieveAPIView, CreateAPIView):
    permission_classes = [HeightRank]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data=return_data_visit(request.user, request.data), status=HTTP_200_OK)
