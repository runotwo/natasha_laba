from django.contrib.auth.models import User
from rest_framework import authentication, permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from goods.models import Good
from orders.models import Order, OrderItem
from .serializers import (GoodsSerializer, UserCreateSerializer, GetTokenSerializer, OrderSerializer, AddCartSerializer)


class GoodView(ReadOnlyModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodsSerializer

    def list(self, request, *args, **kwargs):
        queryset = Good.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            # Some data preprocessing
            data['email'] = data['email'].lower()
            data['username'] = data['email']
            data['first_name'] = data['name']
            del data['name']

            # Check if user already exists
            user_qs = User.objects.filter(username=data['email'], email=data['email'])
            if user_qs.exists():
                return Response(
                    data={'status': 'Error', 'error': 'Пользователь с такими данными уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(**data)
            user.save()
            token = Token.objects.create(user=user)
            return Response(data={'status': 'Ok', 'name': user.first_name, 'token': token.key},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={'status': 'Error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetToken(ObtainAuthToken):
    serializer_class = GetTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class OrderViev(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        last_order = Order.objects.filter(client=request.user).last()
        if not last_order or last_order.status != 'created':
            last_order = Order.objects.create(client=request.user)
        serializer = self.get_serializer(last_order)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        last_order = Order.objects.filter(client=request.user)
        serializer = self.get_serializer(last_order, many=True)
        return Response(serializer.data)


class OrdersViev(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        instance = Order.objects.filter(client=request.user, id=kwargs.get('pk')).last()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartView(mixins.RetrieveModelMixin,
               GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        last_order = Order.objects.filter(client=request.user).last()
        if not last_order or last_order.status != 'created':
            last_order = Order.objects.create(client=request.user)
        return Response(self.get_serializer(last_order).data)

    def post(self, request):
        serializer = AddCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'status': 'Error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        good = Good.objects.get(id=serializer.data['good_id'])
        last_order = Order.objects.filter(client=request.user).last()
        if not last_order or last_order.status != 'created':
            last_order = Order.objects.create(client=request.user)
        order_item = OrderItem.objects.filter(order=last_order, good=good).last()
        if not order_item:
            order_item = OrderItem(order=last_order, good=good)
        order_item.count += 1
        order_item.save()
        return Response(self.get_serializer(last_order).data)

    def delete(self, request, pk, format=None):
        serializer = AddCartSerializer(data={'good_id': pk})
        if not serializer.is_valid():
            return Response(data={'status': 'Error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        good = Good.objects.get(id=serializer.data['id'])
        last_order = Order.objects.filter(client=request.user).last()
        if not last_order or last_order.status != 'created':
            return Response(data={'status': 'Error', 'errors': {'not_found': ['Не найден открытый заказ']}},
                            status=status.HTTP_400_BAD_REQUEST)
        order_item = OrderItem.objects.filter(order=last_order, good=good).last()
        if not order_item:
            return Response(self.serializer_class(last_order).data)
        order_item.count -= 1
        order_item.save()
        return Response(self.get_serializer(last_order).data)
