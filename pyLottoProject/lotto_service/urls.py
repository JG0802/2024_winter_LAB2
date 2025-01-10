from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # auth_views 임포트 추가
from lotto import views as lotto_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 기본 관리자 페이지
    path('', lotto_views.home, name='home'),  # 루트 URL을 home 뷰에 연결
    path('lotto/', include('lotto.urls')),  # lotto 앱 URL 포함
    path('admin/login/', auth_views.LoginView.as_view(template_name='lotto/admin_login.html'), name='admin_login'),  # 관리자 로그인 페이지
]
