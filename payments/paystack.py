import requests
from django.conf import settings


class Paystack:
    """
    Paystack API integration class for initializing and verifying payments.
    """

    base_url: str = settings.PAYSTACK_BASE_URL
    secret_key: str = settings.PAYSTACK_SECRET_KEY

    @classmethod
    def initialize_payment(cls, email: str, amount: float, reference: str) -> dict:
        """
        Initialize a Paystack transaction.

        Args:
            email (str): Customer's email address.
            amount (float): Amount to charge in Naira.
            reference (str): Unique transaction reference.

        Returns:
            dict: Response from Paystack API.
        """
        url = f"{cls.base_url}/transaction/initialize"
        headers = {"Authorization": f"Bearer {cls.secret_key}"}
        data = {"email": email, "amount": int(amount * 100), "reference": reference}

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @classmethod
    def verify_payment(cls, reference: str) -> dict:
        """
        Verify a Paystack transaction.

        Args:
            reference (str): Unique transaction reference.

        Returns:
            dict: Response from Paystack API.
        """
        url = f"{cls.base_url}/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {cls.secret_key}"}

        response = requests.get(url, headers=headers)
        return response.json()
