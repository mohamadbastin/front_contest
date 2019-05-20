from django.urls import path
from rest_framework.authtoken import views

from .views import *

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('signup/', SignupView.as_view()),
    path('book/submit/', SubmitBookView.as_view()),
    path('book/list/', BookListView.as_view()),
    path('book/detail/<int:pk>/', BookDetailView.as_view()),
    path('book/request/<int:pk>/', RequestCreateView.as_view()),
    path('request/list/<sell_pk>/', ListRequestView.as_view()),
    path('request/choose/<int:request_pk>/', SelectRequestView.as_view()),
    path('request/my/', ListMyRequestsView.as_view())
]

    