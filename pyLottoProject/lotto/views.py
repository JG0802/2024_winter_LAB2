from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LottoTicket, WinningNumber
from random import sample

def buy_lotto(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # 사용자 이름 가져오기

        if not name:  # 이름이 비어 있는 경우 에러 처리
            return render(request, 'lotto/buy_lotto.html', {
                'error_message': 'Name field is required!'
            })

        # 자동 생성 버튼 클릭 처리
        if 'auto_generate' in request.POST:
            # 랜덤으로 6개의 번호 생성 (1~45)
            numbers = "-".join(map(str, sample(range(1, 46), 6)))
            LottoTicket.objects.create(name=name, numbers=numbers)  # 데이터 저장
            return redirect('results_user', name=name)  # 결과 페이지로 이동

        # 직접 입력 처리
        elif 'manual_submit' in request.POST:
            # 사용자가 입력한 번호 가져오기
            numbers = "-".join([
                request.POST.get('num1'),
                request.POST.get('num2'),
                request.POST.get('num3'),
                request.POST.get('num4'),
                request.POST.get('num5'),
                request.POST.get('num6'),
            ])
            LottoTicket.objects.create(name=name, numbers=numbers)  # 데이터 저장
            return redirect('results_user', name=name)  # 결과 페이지로 이동

    return render(request, 'lotto/buy_lotto.html')

# 사용자 결과 페이지
def results_user(request, name):
    ticket = LottoTicket.objects.filter(name=name).first()  # 해당 이름의 티켓 가져오기
    winning_number = WinningNumber.objects.latest('id') if WinningNumber.objects.exists() else None

    if winning_number and ticket:
        try:
            # 사용자 번호와 당첨 번호를 정수 집합으로 변환
            ticket_numbers = set(map(int, ticket.numbers.split('-')))
            winning_numbers = set(map(int, winning_number.numbers.split('-')))

            # 교집합 계산
            match_count = len(ticket_numbers & winning_numbers)

            # 당첨 등수 판별
            if match_count == 6:
                match_status = "1등"
            elif match_count == 5:
                match_status = "2등"
            elif match_count == 4:
                match_status = "3등"
            elif match_count == 3:
                match_status = "5등"
            else:
                match_status = "미당첨"
        except ValueError:
            match_status = "번호 형식 오류"
    else:
        match_status = "미추첨"

    return render(request, 'lotto/results_user.html', {
        'ticket': ticket,
        'match_status': match_status,
        'winning_number': winning_number,
    })
    
@login_required
def admin_draw(request):
    # 관리자 페이지에서 추첨 진행
    if WinningNumber.objects.exists():
        draw_disabled = True
    else:
        draw_disabled = False

    if request.method == 'POST':
        # 1부터 45까지의 숫자 6개를 랜덤으로 추첨
        numbers = "-".join(map(str, sample(range(1, 46), 6)))  # 6개의 랜덤 번호 생성
        WinningNumber.objects.create(numbers=numbers)  # 추첨 번호 저장
        return redirect('results_admin')

    return render(request, 'lotto/admin_draw.html', {'draw_disabled': draw_disabled})

def results_admin(request):
    # 모든 사용자의 로또 티켓을 가져오기
    all_tickets = LottoTicket.objects.all()
    winning_number = WinningNumber.objects.latest('draw_date') if WinningNumber.objects.exists() else None

    for ticket in all_tickets:
        if winning_number:
            ticket_numbers = set(map(int, ticket.numbers.split('-')))
            winning_numbers = set(map(int, winning_number.numbers.split('-')))
            match_count = len(ticket_numbers & winning_numbers)
            ticket.match_status = "당첨" if match_count > 0 else "미당첨"
        else:
            ticket.match_status = "미추첨"

    return render(request, 'lotto/results_admin.html', {'all_tickets': all_tickets, 'winning_number': winning_number})

def home(request):
    return render(request, 'lotto/home.html')
