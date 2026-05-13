# ==========================================
# 결제 타입 판별
# ==========================================
def detect_payment_type(barcode):

    is_simple_pay = False
    pay_type_name = "🛍️ 일반 구매"

    if barcode.startswith("880"):

        is_simple_pay = True
        pay_type_name = "🎁 카카오 선물하기"

    elif barcode.startswith("881"):

        is_simple_pay = True
        pay_type_name = "🟩 네이버페이"

    elif barcode.startswith("882"):

        is_simple_pay = True
        pay_type_name = "🟡 카카오페이"

    return is_simple_pay, pay_type_name

