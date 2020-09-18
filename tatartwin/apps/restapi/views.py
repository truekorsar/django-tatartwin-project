from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import TatarSerializer, TatarFullSerializer
from apps.core.models import Tatar


class TatarRetrieveAPI(APIView):
    serializer_class = TatarSerializer

    def get(self, request, word):
        tatar_serializer = self.serializer_class(data={'word': word}, is_authenticated=request.user.is_authenticated)
        if tatar_serializer.is_valid():
            tatar = Tatar.objects.find_twin(word)
            serialized_data = self.serializer_class(tatar).data
            return Response(serialized_data)
        else:
            return Response(tatar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TatarFullRetrieveAPI(TatarRetrieveAPI):
    serializer_class = TatarFullSerializer


class TatarCreateAPI(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tatar.objects.all()
    serializer_class = TatarFullSerializer


class TatarTopAPI(APIView):
    def get(self, request, number):
        tatars = Tatar.objects.top(number)
        tatar_serializer = TatarSerializer(tatars, many=True)
        return Response(tatar_serializer.data)


@api_view(['GET'])
def api_spec(request, format=None):
    return Response({
        'Найти татарское слово (пример)': reverse('twin', request=request, format=format, args=['пример']),
        'Найти татарское слово с полным описанием (пример)': reverse('twin_full', request=request, format=format, args=['пример']),
        'Найти топ N слов': reverse('top', request=request, format=format, args=[3]),
        'Создать татарское слово': reverse('create', request=request, format=format)
    })


