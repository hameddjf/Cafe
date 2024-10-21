from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator

from menu.models import Menu
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name='orders'
    )
    menu_items = models.ManyToManyField(
        Menu,
        through='OrderItem',
        verbose_name=_("menu_items"),
        related_name='orders'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at")
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created_at']

    def __str__(self):
        return f"order {self.id} - {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_items.all())


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('SMALL', _('small')),
        ('LARGE', _('large')),
    ]
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_("order")
    )
    menu_item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name=_("menu_item"),
        related_name='order_items'
    )
    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        default='SMALL',
        verbose_name=_("size")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("quantity")
    )

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.menu_item.name} ({self.get_size_display()}) x {self.quantity}"

    @property
    def total_price(self):
        if self.size == 'SMALL':
            price = self.menu_item.price_small or 0
        else:
            price = self.menu_item.price_large or 0
        return price * self.quantity
