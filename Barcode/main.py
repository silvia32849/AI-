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
def process_checkout():


    # ----------------------------------
    # 코드 스캔
    # ----------------------------------
    print("\n📷 코드 스캔 중...")

    result = scan_product.scan_code()

    if result is None:
        print("코드를 인식하지 못했습니다.")
        return

    barcode = result["data"]
    code_type = result["type"]

    print("코드 종류:", code_type)
    print("데이터:", barcode)

    # ----------------------------------
    # 코드 종류별 처리
    # ----------------------------------

    if code_type == "QRCode":

        print("QR 처리")

    else:

        print("상품 바코드 처리")

    # ----------------------------------
    # 제휴사 조회
    # ----------------------------------
    partner = partner_info.get_partner_info(
        barcode
    )

    if partner is None:
        return

    # ----------------------------------
    # DB 정보 가져오기
    # ----------------------------------
    partner_name = partner["partner_name"]

    partner_discount = partner["discount_rate"]

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
    original_price = 20000

    (
        p_discount_amt,
        t_discount_amt,
        final_price

    ) = calculate_price.calculate_price(

        original_price,
        partner_discount,
        telecom_discount
    )

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

        return

    # ----------------------------------
    # 일반 구매면 결제 선택
    # ----------------------------------
    payment_menu.payment_menu(
        final_price
    )


# ==========================================
# 프로그램 시작
# ==========================================
if __name__ == "__main__":

    process_checkout()