from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation(order_id):
    try:
        order = Order.objects.select_related('user').get(id=order_id)
    except Order.DoesNotExist:
        return f'Order {order_id} does not exist'

    subject = f'Order Confirmation - #{order.id}'
    message = (
        f'Hello {order.user.get_full_name() or order.user.username},\n\n'
        f'Thank you for your order #{order.id}.\n'
        f'Total: {order.total}\n\n'
        'We will update you when the order ships.\n\n'
        'Best regards,\nYour Store'
    )

    if not order.user.email:
        return f'No email for order user: {order.user}'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )
    return f'Email sent for order {order.id}'

@shared_task
def cancel_unpaid_orders(minutes=30):
    cutoff = timezone.now() - timedelta(minutes=minutes)
    qs = Order.objects.filter(status='PENDING', created_at__lt=cutoff)
    count = qs.count()
    qs.update(status='canceled')
    return {'cancelled': count}
