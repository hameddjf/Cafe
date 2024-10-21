from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Menu(MPTTModel):
    parent = TreeForeignKey(
        "self", verbose_name=_("menu"), on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    price_small = models.IntegerField(
        null=True, blank=True, verbose_name=_("price (small)"))
    price_large = models.IntegerField(
        null=True, blank=True, verbose_name=_("price (large)"))
    original_images = models.ImageField(
        null=True, blank=True, upload_to='original_images/')
    resizes_images = ProcessedImageField(
        verbose_name="resizes_images",
        upload_to='resizes_images/',
        processors=[ResizeToFill(300, 400)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True, verbose_name=_("available"))

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menues")
        ordering = ["parent__name", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_menu", kwargs={"slug": self.slug})
