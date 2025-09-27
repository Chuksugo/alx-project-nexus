import requests
from django.conf import settings


class Paystack:
    base_url = settings.PAYSTACK_BASE_URL
    secret_key = settings.PAYSTACK_SECRET_KEY

    @classmethod
    def initialize_payment(cls, email, amount, reference):
        url = f"{cls.base_url}/transaction/initialize"
        headers = {"Authorization": f"Bearer {cls.secret_key}"}
        data = {"email": email, "amount": int(amount * 100), "reference": reference}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def verify_payment(cls, reference):
        url = f"{cls.base_url}/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {cls.secret_key}"}
        response = requests.get(url, headers=headers)
        return response.json()
