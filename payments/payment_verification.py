import logging
from crypto_payment import CryptoPayment

class PaymentVerification:
    def __init__(self):
        self.crypto_payment = CryptoPayment()  # Инициализация класса для работы с криптовалютными платежами

    def verify_payment(self, payment_system, payment_id):
        """
        Проверка статуса платежа
        :param payment_system: Название платёжной системы (coinbase, bitpay, crypto.com, paypal, stripe)
        :param payment_id: Идентификатор платежа для проверки статуса
        :return: Статус платежа
        """
        try:
            status = self.crypto_payment.check_payment_status(payment_system, payment_id)
            return status
        except Exception as e:
            logging.error(f"Ошибка при проверке статуса платежа: {e}")
            return f"Ошибка при проверке статуса платежа: {e}"

    def confirm_payment(self, payment_system, payment_id):
        """
        Подтверждение оплаты, если статус платежа успешен
        :param payment_system: Название платёжной системы
        :param payment_id: Идентификатор платежа для проверки статуса
        :return: Сообщение о подтверждении или ошибке
        """
        status = self.verify_payment(payment_system, payment_id)
        
        if status == "success":
            # Логика для подтверждения оплаты в системе, например, обновление статуса в базе данных
            # Здесь можно добавить действия для уведомления пользователя о успешной оплате
            self.update_payment_status(payment_system, payment_id, "confirmed")
            return "Платеж успешно подтверждён."
        else:
            # Обработка случая, когда платеж не подтверждён
            return f"Оплата не подтверждена. Статус: {status}"

    def update_payment_status(self, payment_system, payment_id, status):
        """
        Обновление статуса платежа в базе данных
        :param payment_system: Название платёжной системы
        :param payment_id: Идентификатор платежа
        :param status: Новый статус платежа (например, "confirmed")
        """
        # Тут нужно добавить логику для обновления статуса в вашей базе данных
        logging.info(f"Обновление статуса для платежа {payment_id} в системе {payment_system}: {status}")
        
        # Пример обновления статуса в базе данных:
        # db.session.query(Payment).filter(Payment.payment_id == payment_id).update({"status": status})
        # db.session.commit()

        # Для примера, мы просто выводим информацию в лог
        logging.info(f"Статус платежа {payment_id} успешно обновлён в базе данных.")

    def handle_payment_webhook(self, payment_system, payment_id):
        """
        Обработка webhook уведомлений от платёжной системы
        :param payment_system: Название платёжной системы
        :param payment_id: Идентификатор платежа для проверки
        :return: Статус обработки
        """
        try:
            status = self.verify_payment(payment_system, payment_id)
            if status == "success":
                self.update_payment_status(payment_system, payment_id, "confirmed")
                return f"Платеж {payment_id} подтверждён."
            else:
                return f"Платеж {payment_id} не подтверждён. Статус: {status}"
        except Exception as e:
            logging.error(f"Ошибка при обработке webhook для платежа {payment_id}: {e}")
            return f"Ошибка при обработке webhook для платежа {payment_id}: {e}"

