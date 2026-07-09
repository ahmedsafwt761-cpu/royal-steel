from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'product_slug', 'status', 'created_at']
    list_filter = ['status', 'product_slug', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message']
    list_editable = ['status']
    
    # عشان يظهر الاسم العربي للمنتج
    def product_name(self, obj):
        return obj.get_product_slug_display()
    product_name.short_description = 'نوع المنتج'