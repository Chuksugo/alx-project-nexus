from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    Handles creation and representation of payment records.
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "customer",
            "amount",
            "reference",
            "status",
            "payment_method",
            "access_code",
            "transaction_date",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "reference",
            "created_at",
            "transaction_date",
            "status",
        ]
