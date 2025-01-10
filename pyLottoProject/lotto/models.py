from django.db import models

# 사용자 로또 티켓
class LottoTicket(models.Model):
    name = models.CharField(max_length=100, default="Anonymous")
    numbers = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    match_status = models.CharField(max_length=50, default="미추첨")

    def __str__(self):
        return f"{self.name}: {self.numbers}"

# 로또 당첨 번호
class WinningNumber(models.Model):
    numbers = models.CharField(max_length=50)  # 당첨 번호 (1-5-10-25-60)
    
    def __str__(self):
        return f"Winning Numbers: {self.numbers}"