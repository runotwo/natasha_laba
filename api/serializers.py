from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (CommonPasswordValidator, MinimumLengthValidator,
                                                     NumericPasswordValidator, UserAttributeSimilarityValidator,
                                                     validate_password)
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import authenticate
from sorl.thumbnail import get_thumbnail

from goods.models import Good
from orders.models import Order, Address


class GoodsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Good
        fields = '__all__'

    def get_image(self, good):
        request = self.context.get('request')
        return request.build_absolute_uri(get_thumbnail(good.image, '500x500', crop='center', quality=99).url)


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField()
    name = serializers.CharField(max_length=30)
    password = serializers.CharField()

    def validate_password(self, value):
        user_attributes = ('username', 'email')
        user = User(username=self._kwargs.get('data').get('name'), email=self._kwargs.get('data').get('email'),
                    password='pass1234')
        password_validators = [MinimumLengthValidator(), UserAttributeSimilarityValidator(user_attributes),
                               CommonPasswordValidator(), NumericPasswordValidator()]
        validate_password(value, user, password_validators)
        return value

    def validate_email(self, value):
        validator = EmailValidator()
        validator(value)
        return value


class GetTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            username = username.lower()
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Неправильный email или пароль'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ('created_at', 'client')

    def get_cart(self, order):
        items = order.orderitem_set.all()
        return [{'count': item.count,
                 'good': GoodsSerializer(item.good, context={'request': self.context.get('request')}).data} for item in
                items]

    def get_address(self, order):
        if order.address:
            return GoodsSerializer(order.address).data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AddCartSerializer(serializers.Serializer):
    good_id = serializers.IntegerField(min_value=1)

    def validate_id(self, value):
        if not Good.objects.filter(id=value):
            raise serializers.ValidationError('Некорректный идентификатор товара')
        return value
