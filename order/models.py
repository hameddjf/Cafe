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
        verbose_name=_("کاربر"),
        related_name='orders'
    )
    menu_items = models.ManyToManyField(
        Menu,
        through='OrderItem',
        verbose_name=_("آیتم‌های منو"),
        related_name='orders'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد")
    )

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارشات")
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.id} - {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_items.all())


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('SMALL', _('کوچک')),
        ('LARGE', _('بزرگ')),
    ]
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_("سفارش")
    )
    menu_item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name=_("آیتم منو"),
        related_name='order_items'
    )
    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES,
        default='SMALL',
        verbose_name=_("سایز")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("تعداد")
    )

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم‌های سفارش")

    def __str__(self):
        return f"{self.menu_item.name} ({self.get_size_display()}) x {self.quantity}"

    @property
    def total_price(self):
        if self.size == 'SMALL':
            price = self.menu_item.price_small or 0
        else:
            price = self.menu_item.price_large or 0
        return price * self.quantity

# class Order(models.Model):
#     SIZE_CHOICES = [
#         ('SMALL', _('کوچک')),
#         ('LARGE', _('بزرگ')),
#     ]
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         verbose_name=_("کاربر"),
#         related_name='orders'
#     )
#     menu_item = models.ManyToManyField(
#         Menu,
#         verbose_name=_("آیتم منو"),
#         related_name='orders'
#     )
#     size = models.CharField(
#         max_length=5, choices=SIZE_CHOICES, default='SMALL', verbose_name=_("سایز"))
#     quantity = models.PositiveIntegerField(
#         default=1,
#         validators=[MinValueValidator(1)],
#         verbose_name=_("تعداد")
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_("تاریخ ایجاد")
#     )

#     class Meta:
#         verbose_name = _("سفارش")
#         verbose_name_plural = _("سفارشات")
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"سفارش {self.id} - {self.user.username} - {self.menu_item.name} ({self.get_size_display()})"

#     @property
#     def total_price(self):
#         total = 0
#         for item in self.menu_item.all():
#             if self.size == 'SMALL':
#                 price = item.price_small or 0
#             else:
#                 price = item.price_large or 0
#             total += price * self.quantity
#         return total
