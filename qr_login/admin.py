from django.contrib import admin

from .models import QRCode

# Register your models here.


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    readonly_fields = ('qr_code',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set the user when creating a new QRCode
            obj.user = form.cleaned_data['user']
        super().save_model(request, obj, form, change)
