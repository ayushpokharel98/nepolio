from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.JSONField(default=dict)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    class Meta:
        ordering = ['user']
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
