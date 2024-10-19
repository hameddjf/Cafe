import qrcode
from io import BytesIO
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from django.core.files import File

# Create your models here.


class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code for {self.user.username}"

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(version=1, box_size=15, border=5,
                           error_correction=qrcode.constants.ERROR_CORRECT_H)
        current_site = Site.objects.get_current()
        login_url = f"/login/{self.user.username}/"
        full_url = f"https://{current_site.domain}{login_url}"
        qr.add_data(full_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        canvas = Image.new('RGB', (700, 700), 'white')
        canvas.paste(img)
        filename = f'qr_code-{self.user.username}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(filename, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
