import requests
import time
import db
import discount
import partner_info
import payment
import receipt
import scan_product
import payment_menu
import calculate_price
import pay_balance
import simple_payment






# ==========================================
# 메인 실행
# ==========================================
def process_checkout():

    # 상품 스캔
    barcode = scan_product.scan_product()

    # 결제 타입 판별
    is_simple_pay, pay_type_name = (
        payment.detect_payment_type(barcode)
    )

    # 통신사 할인
    telecom, telecom_discount = (
    discount.process_telecom_discount(
        barcode
    )
)

    print("\n🔍 데이터 확인 중...\n")
    time.sleep(1)

    # 제휴사 조회
    partner = partner_info.get_partner_info(barcode)

    if partner is None:
        return

    partner_name = partner["partner_name"]
    partner_discount = partner["discount_rate"]

    # 가격 계산
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

    # 영수증 출력
    receipt.print_receipt(
        partner_name,
        pay_type_name,
        original_price,
        p_discount_amt,
        telecom,
        t_discount_amt,
        final_price
    )

    # 결제 선택 화면
    payment_menu.payment_menu(
        is_simple_pay,
        pay_type_name,
        final_price
    )


# ==========================================
# 프로그램 시작
# ==========================================
if __name__ == "__main__":

    process_checkout()