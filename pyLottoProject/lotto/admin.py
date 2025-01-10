from django.contrib import admin
from .models import LottoTicket, WinningNumber
from random import sample


class WinningNumberAdmin(admin.ModelAdmin):
    list_display = ('numbers',)  # 당첨 번호만 표시
    change_list_template = "admin/winning_number_changelist.html"  # 커스텀 템플릿 연결

    def changelist_view(self, request, extra_context=None):
        """
        change_list.html에서 POST 요청 처리
        """
        if request.method == "POST" and "draw" in request.POST:
            self.draw_winning_number(request)
        return super().changelist_view(request, extra_context=extra_context)

    def draw_winning_number(self, request):
        """
        새로운 당첨 번호 생성
        """
        if WinningNumber.objects.exists():
            self.message_user(request, "이미 당첨 번호가 존재합니다. 새로운 번호를 생성할 수 없습니다.")
            return
        numbers = "-".join(map(str, sample(range(1, 46), 6)))  # 1~45 사이의 랜덤 6개 번호 생성
        WinningNumber.objects.create(numbers=numbers)  # 새로운 번호 저장
        self.message_user(request, f"새로운 당첨 번호 {numbers}가 생성되었습니다.")

    def has_add_permission(self, request):
        """
        당첨 번호가 이미 존재하면 추가 버튼을 숨김
        """
        return not WinningNumber.objects.exists()  # 기존 번호가 없을 때만 추가 가능


class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'numbers', 'match_status')  # 사용자 이름, 번호, 당첨 여부 표시
    search_fields = ('name',)  # 이름으로 검색 가능
    list_filter = ('match_status',)  # 당첨 여부로 필터링

    def get_queryset(self, request):
        """
        당첨 번호와 사용자 번호를 비교하여 당첨 여부를 설정
        """
        queryset = super().get_queryset(request)
        winning_number = WinningNumber.objects.latest('id') if WinningNumber.objects.exists() else None

        for ticket in queryset:
            if winning_number:
                try:
                    # 사용자 번호와 당첨 번호를 정수 집합으로 변환
                    ticket_numbers = set(map(int, ticket.numbers.split('-')))
                    winning_numbers = set(map(int, winning_number.numbers.split('-')))

                    # 교집합 계산
                    match_count = len(ticket_numbers & winning_numbers)

                    # 당첨 등수 판별
                    if match_count == 6:
                        ticket.match_status = "1등"
                    elif match_count == 5:
                        ticket.match_status = "2등"
                    elif match_count == 4:
                        ticket.match_status = "3등"
                    elif match_count == 3:
                        ticket.match_status = "4등"
                    else:
                        ticket.match_status = "미당첨"
                except ValueError:
                    ticket.match_status = "번호 형식 오류"
                ticket.save()  # 데이터베이스에 상태 저장
            else:
                ticket.match_status = "미추첨"
                ticket.save()  # 데이터베이스에 상태 저장

        return queryset


admin.site.register(WinningNumber, WinningNumberAdmin)
admin.site.register(LottoTicket, LottoTicketAdmin)