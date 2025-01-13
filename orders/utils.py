from datetime import datetime

from django.http import JsonResponse

from orders.vnpay import vnpay
from django.conf import settings

class Util:
    @staticmethod
    def post_payment(order, request):
        base_url = request.build_absolute_uri('/')[:-1].strip("/")  # Sử dụng request để lấy URL
        order_type = 'billpayment'
        order_uuid = order.order_uuid
        amount = int(order.amount)
        order_desc = 'Thanh toán hóa đơn'
        language = 'vn'
        ipaddr = request.META.get('REMOTE_ADDR')  # Lấy IP từ request

        vnp = vnpay()
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_Amount'] = amount * 100
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_Locale'] = language if language else 'vn'
        vnp.requestData['vnp_TxnRef'] = str(order_uuid)
        vnp.requestData['vnp_OrderInfo'] = order_desc
        vnp.requestData['vnp_OrderType'] = order_type
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_IpAddr'] = ipaddr
        vnp.requestData['vnp_ReturnUrl'] = f'{base_url}{settings.VNPAY_RETURN_URL}'

        vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
        return vnpay_payment_url