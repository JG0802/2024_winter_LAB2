from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 초기 홈 페이지
    path('buy/', views.buy_lotto, name='buy_lotto'),  # 일반 사용자 로또 입력 페이지
    path('results/<str:name>/', views.results_user, name='results_user'),  # 일반 사용자 결과 확인 페이지
    path('admin/draw/', views.admin_draw, name='admin_draw'),  # 관리자 추첨 페이지
    path('results/admin/', views.results_admin, name='results_admin'),  # 관리자 결과 확인 페이지
]
