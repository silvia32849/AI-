import time

import discount
import partner_info
import receipt
import payment_menu
import calculate_price
import simple_payment


# ==========================================
# 메인 실행
# ==========================================
def process_checkout(
    barcode,
    original_price,
    discounted_price=None
):

    print("바코드:", barcode)

    # ----------------------------------
    # 할인 적용 가격 우선 사용
    # ----------------------------------

    if discounted_price is not None:
        original_price = discounted_price

    # ----------------------------------
    # 코드 종류 판별
    # ----------------------------------

    if (
        barcode.startswith("QR")
        or "PAY" in barcode.upper()
    ):

        code_type = "QRCode"

    else:

        code_type = "Barcode"

    print("코드 종류:", code_type)
    print("데이터:", barcode)

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

    partner_name = partner.get(
        "partner_name",
        "알 수 없음"
    )

    partner_discount = partner.get(
        "discount_rate",
        0
    )

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
        partner_name,
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
    # React 반환
    # ----------------------------------

    return {

        "success": True,

        "barcode": barcode,

        "code_type": code_type,

        "partner_name": partner_name,

        "payment_type": pay_type_name,

        "partner_discount": p_discount_amt,

        "telecom": telecom,

        "telecom_discount": t_discount_amt,

        "original_price": original_price,

        "final_price": final_price,

        "is_simple_pay": is_simple_pay,

        "originalPrice": original_price,

        "discountedPrice": final_price
    
    }