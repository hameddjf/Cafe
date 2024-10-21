from mptt.admin import DraggableMPTTAdmin

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import Menu

# Register your models here.
from django.contrib.auth.models import Group
admin.site.unregister(Group)


class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1
    fields = ('name', 'slug', 'price_small', 'price_large', 'resizes_images')
    show_change_link = True


@admin.register(Menu)
class MenuAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'price_small', 'price_large', 'slug',
                    'resizes_image', 'original_image', 'available')
    list_display_links = ('indented_title',)
    list_filter = ('parent', 'available')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuInline]

    fieldsets = (
        (None, {
            'fields': ('parent', 'name', 'slug', 'price_small', 'price_large', 'description', 'available')
        }),
        (_('تصاویر'), {
            'fields': ('original_images', 'resizes_images')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')

    @admin.display(description=_('resizes_image'))
    def resizes_image(self, obj):
        if obj.resizes_images:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;"/>',
                obj.resizes_images.url
            )
        return "-"

    @admin.display(description=_('original_image'))
    def original_image(self, obj):
        if obj.original_images:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;"/>',
                obj.original_images.url
            )
        return "-"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['parent'].queryset = Menu.objects.exclude(
                pk=obj.pk)  # .exclude(descendant_of=obj)
        return form

    def indented_title(self, item):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            item.level * self.mptt_level_indent,
            item.name,
        )
    indented_title.short_description = _('parent')
