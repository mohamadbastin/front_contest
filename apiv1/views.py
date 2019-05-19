from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status

from .models import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView, CreateAPIView, RetrieveAPIView, \
    UpdateAPIView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.messages import SUCCESS, ERROR, get_messages
from django.contrib import messages
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .permission_classes import *


class OnlyOneRequestPerSell(BasePermission):
    message = 'You already requested this sell'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        # print("is post: ", request.method)
        profile = request.user.profile
        sell = Sell.objects.get(pk=view.kwargs.get('pk'))
        p = profile.buy_request.filter(sell=sell)

        if p:
            return False
        return True


class NotSelfRequest(BasePermission):
    message = 'you cant request your own book'

    def has_permission(self, request, view):
        # if request.method != 'POST':
        #     return True
        #
        # try:
        # print(request.method)
        sender = request.user.profile
        # print("pk: ", view.kwargs.get('pk'))
        profile = Sell.objects.get(pk=view.kwargs.get('pk')).profile

        if sender == profile:
            return False
        return True
        # except KeyError:
        #     return True
        # except Sell.DoesNotExist:
        #     return True
        # except:
        #     return True


class CreateNotSold(BasePermission):
    message = 'this book has already been sold'

    def has_permission(self, request, view):
        # print('in here')
        # print(view)
        # print(RequestCreateView.as_view() == view)
        # if view == RequestCreateView:
        _request = get_object_or_404(Sell, pk=view.kwargs.get('pk'))
        # print('passed')
        # print(_request)
        if _request.is_available:
            return True
        return False

        # print('yo')


class SelectNotSold(BasePermission):
    message = 'this book has already been sold'

    def has_permission(self, request, view):
        # print('baby')
        _request = get_object_or_404(Request, pk=view.kwargs.get('request_pk'))
        sell = _request.sell
        if sell.is_available:
            return True
        return False


class IsSelfRequest(BasePermission):
    message = 'you don\'t have permission for this books requests.'

    def has_permission(self, request, view):
        profile = request.user.profile
        # print("pk: ", view.kwargs.get('pk'))
        # profile = Sell.objects.get(pk=view.kwargs.get('pk')).profile
        sell_pk = view.kwargs.get('sell_pk', None)

        sell = get_object_or_404(Sell, pk=sell_pk)

        if profile == sell.profile:
            return True
        return False


class IsSellProfile(BasePermission):
    def has_permission(self, request, view):
        print('here')
        _request = get_object_or_404(Request, pk=view.kwargs.get('request_pk'))
        print('passed')
        if _request.sell.profile == request.user.profile:
            return True
        return False


class SignupView(CreateAPIView):
    serializer_class = ProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        r = self.serializer_class(data=request.data)

        if r.is_valid():
            p = r.save()

            rd = ProfileDetailSerializer(p).data

            return Response(rd)
        else:
            return Response(r.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitBookView(CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile

        s = self.serializer_class(data=request.data, context={'profile': profile})

        if s.is_valid():
            s.save()

            return Response(s.data)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'profile',
        'book_state',
        'title',
        'author',
        'translator',
        'publisher',
        'chap',
        'date_published',
        'pages',
        'description')


class BookDetailView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class RequestCreateView(CreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, OnlyOneRequestPerSell, NotSelfRequest, CreateNotSold]

    allowed_methods = ['POST', ]

    def post(self, request, *args, **kwargs):
        sender = request.user.profile

        r = self.serializer_class(data=request.data, context={'sender': sender})

        if r.is_valid():
            r.save()

            return Response(r.data)
        else:
            return Response(r.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRequestView(ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, IsSelfRequest]

    def get_queryset(self):
        profile = self.request.user.profile
        sell = self.kwargs.get('sell_pk', None)
        sell = get_object_or_404(Sell, pk=sell)
        return Request.objects.filter(sell=sell)


class SelectRequestView(GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, SelectNotSold, IsSellProfile]

    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        _request = get_object_or_404(Request, pk=kwargs.get('request_pk'))
        _request.status = "sold"
        _request.save()
        sell = get_object_or_404(Sell, pk=_request.sell.pk)

        for r in sell.request.filter(~Q(pk=_request.pk)):
            r.status = "declined"
            r.save()

        return Response({'success': 'Request Accepted'})


class ListMyRequestsView(ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        profile = self.request.user.profile
        list = Request.objects.filter(sender=profile)
        return list
