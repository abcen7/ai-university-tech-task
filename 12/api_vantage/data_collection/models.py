from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date_time = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.symbol} at {self.date_time}"
