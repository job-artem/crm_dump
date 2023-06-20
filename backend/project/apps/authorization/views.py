from django.http import JsonResponse, QueryDict, FileResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import TokenUserSerializer, RegistrationUserSerializer, LoginUserSerializer, UserDataSerializer, \
    EditProfileSerializer
from .utils.auth import confirm_user, registration_user, login_user
from .utils.edit import clear_data, update_user_data, get_time
from .utils.renderers import renderer_user


class LoginUserAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = [TokenUserSerializer, LoginUserSerializer]

    def validate_data(self, data: QueryDict) -> dict or bool:
        for serializer in self.serializer_class:
            serializer_data = serializer(data=data)
            if serializer_data.is_valid():
                return {**serializer_data.validated_data}
        return False

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.validate_data(request.data)
        if not data:
            return JsonResponse(data={'error': 'InvalidData'}, status=HTTP_400_BAD_REQUEST)
        data = login_user(data)
        return JsonResponse(data=data, status=HTTP_400_BAD_REQUEST if 'error' in data else HTTP_200_OK)


class RegistrationUserAPI(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = [TokenUserSerializer, RegistrationUserSerializer]

    def validate_data(self, data: QueryDict) -> dict or bool:
        for serializer in self.serializer_class:
            serializer_data = serializer(data=data)
            if serializer_data.is_valid():
                return {**serializer_data.validated_data}
        return False

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.validate_data(request.data)
        if not data:
            return JsonResponse(data={'error': 'InvalidData'}, status=HTTP_400_BAD_REQUEST)
        if isinstance(data := registration_user(data), bool):
            return JsonResponse(data={'registration': 'success'}, status=HTTP_201_CREATED)
        return JsonResponse(data=data, status=HTTP_400_BAD_REQUEST)


class ConfirmAPI(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenUserSerializer

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.serializer_class(data=request.data)
        if not data.is_valid():
            return JsonResponse(data={}, status=HTTP_400_BAD_REQUEST)
        if confirm_user({**data.validated_data}['token']):
            return JsonResponse(data=data.validated_data, status=HTTP_200_OK)
        return JsonResponse(data={'error': 'InvalidToken'}, status=HTTP_400_BAD_REQUEST)


class AdminAPI(RetrieveAPIView):
    permission_classes = (IsAdminUser,)


class UserDataApi(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = [UserDataSerializer, EditProfileSerializer]

    def serialize_data(self, data: dict) -> dict or bool:
        for serializer in self.serializer_class:
            data_serializer = serializer(data=data)
            if data_serializer.is_valid():
                return {**data_serializer.validated_data}

        return False

    def get(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.serialize_data(data=renderer_user(user=request.user))
        return JsonResponse(data=data, status=HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = self.serialize_data(data=clear_data(request.data))
        update_user_data(data, request.user)
        return JsonResponse(data={}, status=HTTP_200_OK)


class ImageAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs) -> FileResponse:
        image = request.user.image
        response = FileResponse(open(image.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename={image.name}'
        return response


class TimeGetAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data={'time': get_time()}, status=HTTP_200_OK)
