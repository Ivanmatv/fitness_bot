import requests
import json
from config import COINBASE_COMMERCE_API_KEY, BITPAY_API_KEY, CRYPTOCOM_API_KEY, PAYPAL_CLIENT_ID, PAYPAL_SECRET, STRIPE_API_KEY

class CryptoPayment:
    def __init__(self):
        self.coinbase_api_url = "https://api.commerce.coinbase.com/charges"
        self.bitpay_api_url = "https://bitpay.com/api/invoices"
        self.cryptocom_api_url = "https://api.crypto.com/v2/payment"
        self.paypal_api_url = "https://api.sandbox.paypal.com/v1/payments/payment"
        self.stripe_api_url = "https://api.stripe.com/v1/charges"
        self.coinbase_api_key = COINBASE_COMMERCE_API_KEY
        self.bitpay_api_key = BITPAY_API_KEY
        self.cryptocom_api_key = CRYPTOCOM_API_KEY
        self.paypal_client_id = PAYPAL_CLIENT_ID
        self.paypal_secret = PAYPAL_SECRET
        self.stripe_api_key = STRIPE_API_KEY

    def create_payment(self, amount, currency="USD", crypto_type="BTC", description="Подписка на тренировку", payment_system="coinbase"):
        if payment_system == "coinbase":
            return self.create_coinbase_payment(amount, currency, crypto_type, description)
        elif payment_system == "bitpay":
            return self.create_bitpay_payment(amount, currency, crypto_type, description)
        elif payment_system == "crypto.com":
            return self.create_cryptocom_payment(amount, currency, crypto_type, description)
        elif payment_system == "paypal":
            return self.create_paypal_payment(amount, currency, description)
        elif payment_system == "stripe":
            return self.create_stripe_payment(amount, currency, description)
        else:
            return "Ошибка: Неизвестная платёжная система"

    def create_coinbase_payment(self, amount, currency, crypto_type, description):
        headers = {
            "X-CC-Api-Key": self.coinbase_api_key,
            "X-CC-Api-Version": "2018-03-22",
            "Content-Type": "application/json"
        }

        data = {
            "name": "Fitness Bot Subscription",
            "description": description,
            "pricing_type": "fixed_price",
            "local_price": {
                "amount": str(amount),
                "currency": currency
            },
            "payment_method": {"coin": crypto_type},
            "redirect_url": "https://your-redirect-url.com/success",
            "cancel_url": "https://your-redirect-url.com/cancel"
        }

        response = requests.post(self.coinbase_api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            charge = response.json()
            return charge["data"]["hosted_url"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def create_bitpay_payment(self, amount, currency, crypto_type, description):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bitpay_api_key}"
        }

        data = {
            "price": amount,
            "currency": currency,
            "token": crypto_type,
            "posData": description,
            "redirectUrl": "https://your-redirect-url.com/success",
            "cancelUrl": "https://your-redirect-url.com/cancel"
        }

        response = requests.post(self.bitpay_api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            invoice = response.json()
            return invoice["data"]["url"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def create_cryptocom_payment(self, amount, currency, crypto_type, description):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.cryptocom_api_key}"
        }

        data = {
            "amount": amount,
            "currency": currency,
            "coin": crypto_type,
            "description": description,
            "success_url": "https://your-redirect-url.com/success",
            "cancel_url": "https://your-redirect-url.com/cancel"
        }

        response = requests.post(self.cryptocom_api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            payment_link = response.json()
            return payment_link["data"]["paymentUrl"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def create_paypal_payment(self, amount, currency, description):
        auth = self.get_paypal_auth()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth['access_token']}"
        }

        data = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": currency
                },
                "description": description
            }],
            "redirect_urls": {
                "return_url": "https://your-redirect-url.com/success",
                "cancel_url": "https://your-redirect-url.com/cancel"
            }
        }

        response = requests.post(self.paypal_api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            payment = response.json()
            approval_url = next(link['href'] for link in payment['links'] if link['rel'] == 'approval_url')
            return approval_url
        else:
            return f"Error: {response.status_code} - {response.text}"

    def create_stripe_payment(self, amount, currency, description):
        headers = {
            "Authorization": f"Bearer {self.stripe_api_key}"
        }

        data = {
            "amount": int(amount * 100),  # Stripe ожидает сумму в центах
            "currency": currency,
            "description": description,
            "source": "tok_visa"  # Замените на источник платежа
        }

        response = requests.post(self.stripe_api_url, headers=headers, data=data)

        if response.status_code == 200:
            charge = response.json()
            return charge["id"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def get_paypal_auth(self):
        """
        Получение токена авторизации для PayPal
        """
        auth = requests.auth.HTTPBasicAuth(self.paypal_client_id, self.paypal_secret)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token", headers=headers, auth=auth, data="grant_type=client_credentials")
        return response.json()

    def check_payment_status(self, payment_system, payment_id):
        if payment_system == "coinbase":
            return self.check_coinbase_payment_status(payment_id)
        elif payment_system == "bitpay":
            return self.check_bitpay_payment_status(payment_id)
        elif payment_system == "crypto.com":
            return self.check_cryptocom_payment_status(payment_id)
        elif payment_system == "paypal":
            return self.check_paypal_payment_status(payment_id)
        elif payment_system == "stripe":
            return self.check_stripe_payment_status(payment_id)
        else:
            return "Ошибка: Неизвестная платёжная система"

    def check_coinbase_payment_status(self, charge_id):
        headers = {
            "X-CC-Api-Key": self.coinbase_api_key,
            "X-CC-Api-Version": "2018-03-22"
        }

        response = requests.get(f"{self.coinbase_api_url}/{charge_id}", headers=headers)

        if response.status_code == 200:
            charge = response.json()
            status = charge["data"]["timeline"][-1]["status"]
            return status
        else:
            return f"Error: {response.status_code} - {response.text}"

    def check_bitpay_payment_status(self, invoice_id):
        headers = {
            "Authorization": f"Bearer {self.bitpay_api_key}"
        }

        response = requests.get(f"{self.bitpay_api_url}/{invoice_id}", headers=headers)

        if response.status_code == 200:
            invoice = response.json()
            status = invoice["data"]["status"]
            return status
        else:
            return f"Error: {response.status_code} - {response.text}"

    def check_cryptocom_payment_status(self, payment_id):
        headers = {
            "Authorization": f"Bearer {self.cryptocom_api_key}"
        }

        response = requests.get(f"{self.cryptocom_api_url}/{payment_id}", headers=headers)

        if response.status_code == 200:
            payment = response.json()
            status = payment["data"]["status"]
            return status
        else:
            return f"Error: {response.status_code} - {response.text}"

    def check_paypal_payment_status(self, payment_id):
        auth = self.get_paypal_auth()

        headers = {
            "Authorization": f"Bearer {auth['access_token']}"
        }

        response = requests.get(f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}", headers=headers)

        if response.status_code == 200:
            payment = response.json()
            status = payment["state"]
            return status
        else:
            return f"Error: {response.status_code} - {response.text}"

    def check_stripe_payment_status(self, charge_id):
        headers = {
            "Authorization": f"Bearer {self.stripe_api_key}"
        }

        response = requests.get(f"https://api.stripe.com/v1/charges/{charge_id}", headers=headers)

        if response.status_code == 200:
            charge = response.json()
            status = charge["status"]
            return status
        else:
            return f"Error: {response.status_code} - {response.text}"
