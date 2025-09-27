import uuid
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Payment
from orders.models import Order
from .paystack import Paystack


def initialize_payment(request, order_id):
    """
    Initialize a Paystack payment for a given order.
    """
    order = get_object_or_404(Order, id=order_id)
    reference = str(uuid.uuid4()).replace("-", "")[:12]  # generate unique reference

    payment = Payment.objects.create(
        order=order,
        customer=request.user,
        amount=order.total_amount,  # ensure Order model has total_amount field
        email=request.user.email,
        reference=reference,
    )

    paystack = Paystack.initialize_payment(payment.email, payment.amount, payment.reference)

    if paystack.get("status"):
        payment.access_code = paystack["data"]["access_code"]
        payment.save()
        return JsonResponse({"authorization_url": paystack["data"]["authorization_url"]})
    return JsonResponse({"error": "Payment initialization failed"}, status=400)


def verify_payment(request, reference):
    """
    Verify a Paystack payment and update Payment + Order records.
    """
    paystack = Paystack.verify_payment(reference)

    if not paystack.get("status"):
        return JsonResponse({"error": "Verification failed"}, status=400)

    data = paystack.get("data", {})
    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment record not found"}, status=404)

    # Update payment based on Paystack response
    if data.get("status") == "success":
        payment.status = "success"
        payment.transaction_date = data.get("transaction_date")
        payment.save()

        # Update related order
        order = payment.order
        order.payment_status = "paid"
        order.status = "processing"  # workflow customization
        order.save()

        return JsonResponse({"message": "Payment verified", "status": payment.status})

    # Handle failed payments
    payment.status = "failed"
    payment.save()

    order = payment.order
    order.payment_status = "failed"
    order.save()

    return JsonResponse({"message": "Payment failed"}, status=400)
