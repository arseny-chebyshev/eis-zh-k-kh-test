import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Accrual(models.Model):
    date = models.DateField(auto_now=False, blank=False)
    month = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    is_paid = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.date)

    def save(self, *args, **kwargs):
        date = datetime.date.fromisoformat(str(self.date))
        self.month = int(date.month)
        super().save(*args, **kwargs)
    
class Payment(models.Model):
    date = models.DateField(verbose_name="Дата платежа (в формате даты долга)", auto_now=False, blank=False)
    month = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    accrual = models.ForeignKey(Accrual, on_delete=models.DO_NOTHING, blank=True, null=True)
    has_accrual = models.BooleanField(default=False)

    def get_accrual(self) -> Accrual:
        same_month_accruals = Accrual.objects.filter(month=self.month).filter(date__lt=self.date).filter(is_paid=False)
        if not same_month_accruals:
            earliest_accrual = Accrual.objects.filter(date__lt=self.date).filter(is_paid=False).order_by('date').first()
        else:
            earliest_accrual = same_month_accruals.filter(date__lt=self.date).filter(is_paid=False).order_by('date').first()
        return earliest_accrual

    def _pay_accrual(self):
        if self.accrual:
            self.accrual.is_paid = True
            self.accrual.save()        

    def __str__(self) -> str:
        return str(self.date)

    def save(self, *args, **kwargs):
        date = datetime.date.fromisoformat(str(self.date))
        self.month = int(date.month)
        accrual = self.get_accrual()
        if accrual:
            self.accrual = accrual
            self.has_accrual = True
            self._pay_accrual()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.has_accrual:
            accrual = self.accrual
            accrual.is_paid = False
            accrual.save()
        super().delete()
