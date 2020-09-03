from rest_framework import serializers
from .models import Task, Sprint
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'due_date',
            'effort',
            'blocked_by',
            'state',
            'created',
            'last_updated',
            'owner',
        ]

    owner = serializers.ReadOnlyField(source='owner.username')


    


class SprintSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'id',
            'title',
            'state',
            'started',
            'finished',
            'tasks',
            'created',
            'last_updated',
            'owner',
        ]

    owner = serializers.ReadOnlyField(source='owner.username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')