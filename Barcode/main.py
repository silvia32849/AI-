import time

import discount
import partner_info
import receipt
import scan_product
import payment_menu
import calculate_price
import simple_payment


# ==========================================
# 메인 실행
# ==========================================
# ==========================================
# 메인 실행
# ==========================================
def process_checkout(barcode, original_price, discounted_price=None):

    if discounted_price:
        original_price = discounted_price

    print("바코드:", barcode)

    # ----------------------------------
    # QR 스캔
    # ----------------------------------

    print("\nQR 인식 성공!")
    print(f"데이터: {barcode}")

    # ----------------------------------
    # 제휴사 조회
    # ----------------------------------

    partner = partner_info.get_partner_info(
        barcode
    )

    if partner is None:
        return {
            "error": "제휴사 없음"
        }

    # ----------------------------------
    # DB 정보 가져오기
    # ----------------------------------

    partner_name = partner["partner_name"]

    partner_discount = partner["discount_rate"]
    partner_discount = 0

    is_simple_pay = partner.get(
        "is_simple_pay",
        False
    )

    pay_type_name = partner.get(
        "payment_type",
        "🛍️ 일반 구매"
    )

    # ----------------------------------
    # 통신사 할인
    # ----------------------------------

    telecom, telecom_discount = (
        discount.process_telecom_discount(
            barcode
        )
    )

    print("\n🔍 데이터 확인 중...\n")
    time.sleep(1)

    
    # ----------------------------------
    # 가격 계산
    # ----------------------------------

   

    
    (
        p_discount_amt,
        t_discount_amt,
        final_price

    ) = calculate_price.calculate_price(

        original_price,
        partner_discount,
        telecom_discount
    )
    print("partner:", p_discount_amt)
    print("telecom:", t_discount_amt)
    print("final:", final_price)
    # ----------------------------------
    # 영수증 출력
    # ----------------------------------

    receipt.print_receipt(

        partner_name,

        pay_type_name,

        original_price,

        p_discount_amt,

        telecom,

        t_discount_amt,

        final_price
    )

    # ----------------------------------
    # 간편결제 QR이면 바로 결제
    # ----------------------------------

    if is_simple_pay:

        simple_payment.process_simple_payment(
            pay_type_name,
            final_price
        )

    # ----------------------------------
    # React로 데이터 반환
    # ----------------------------------

    return {
        "barcode": barcode,
        "partner_name": partner_name,
        "telecom_discount": t_discount_amt,
        "final_price": final_price,
        "original_price": original_price,
        "telecom": telecom,
        "payment_type": pay_type_name,
        "is_simple_pay": is_simple_pay,
    }