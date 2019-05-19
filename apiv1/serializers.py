from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from users.models import Profile


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Profile
        fields = ['pk','user', 'email', 'phone_number', 'info', 'first_name',
                  'last_name', 'student_number', 'code_melli', 'bank_account']


class ProfileCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Profile
        fields = ['pk','username', 'password', 'email', 'phone_number', 'info', 'first_name',
                  'last_name', 'student_number', 'code_melli', 'bank_account']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.pop('username', None),
                                        password=validated_data.pop('password', None))

        profile = Profile(**validated_data)
        profile.user = user
        profile.save()

        return profile


class BookSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['pk',
            'profile',
            'book_state',
            'title',
            'author',
            'translator',
            'publisher',
            'chap',
            'date_published',
            'pages',
            'description'
        ]

        read_only_fields = ['profile', ]

    def create(self, validated_data):
        profile = self.context.get('profile', None)

        book = Book(**validated_data)
        book.profile = profile

        book.save()

        return book


class RequestSerializer(serializers.ModelSerializer):
    sender = ProfileDetailSerializer(read_only=True)
    book = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['pk','sender', 'sell', 'book', 'status']
        read_only_fields = ['sender', 'book', 'status']

        extra_kwargs = {'sell': {'write_only': True}}

    @staticmethod
    def get_book(instance):
        return BookSerializer(instance=instance.sell.book).data

    def create(self, validated_data):
        sender = self.context.get('sender', None)

        request = Request(**validated_data)
        request.sender = sender

        request.save()

        return request

