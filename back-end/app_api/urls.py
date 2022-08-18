from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/get-user-data/', views.GetUserData.as_view()),
    path('api/v1/card-management/', views.CardManagement.as_view()),
    path('api/v1/transaction-management/', views.TransactionManagement.as_view()),
    path('api/v1/get-last-version/', views.GetLastVersion.as_view()),
    path('api/v1/profile-collector/', views.ProfileCollector.as_view()),
    path('api/v1/info-update/', views.InfoUpdateView.as_view()),
    path('api/v1/print-account/', views.PrintAccount.as_view()),
    path('api/v1/create-guest/', views.CreateGuestView.as_view()),
    path('api/v1/get-chart/', views.GetChartApiView.as_view()),
]