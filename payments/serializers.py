from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "reference", "created_at", "transaction_date", "status"]
