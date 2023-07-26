from users.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            CustomUser.USERNAME_FIELD,
            'password',
        )

class CustomUserSerializer(UserSerializer):
    # is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            # 'is_subscribed',
        )