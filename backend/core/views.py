from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from .models import Quote
from .serializers import QuoteSerializer


class QuoteRateThrottle(AnonRateThrottle):
    rate = '10/hour'


class QuoteCreateView(generics.CreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    throttle_classes = [QuoteRateThrottle]

    def perform_create(self, serializer):
        quote = serializer.save()

        # Send email notification in production
        if not settings.DEBUG:
            try:
                send_mail(
                    subject=f'طلب عرض سعر جديد - {quote.name}',
                    message=f'''
                    اسم: {quote.name}
                    تليفون: {quote.phone}
                    منتج: {quote.get_product_slug_display()}
                    رسالة: {quote.message}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['royalsteelegypt@gmail.com'],
                    fail_silently=True,
                )
            except Exception:
                pass

        return quote


class QuoteListView(generics.ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer