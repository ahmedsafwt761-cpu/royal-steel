from rest_framework import serializers
from .models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='get_product_slug_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Quote
        fields = [
            'id', 'product_slug', 'product_name', 'name', 'phone',
            'email', 'company', 'message', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']