import simple_payment
import scan_product


# ==========================================
# 간편결제 종류 판별
# ==========================================
def detect_payment_type(barcode):

    if barcode.startswith("880"):

        return "네이버페이"

    elif barcode.startswith("281"):

        return "카카오페이"

    else:

        return "일반 간편결제"


# ==========================================
# 결제 메뉴
# ==========================================
def payment_menu(final_price):

    while True:

        print("\n=== 결제 수단 선택 ===")

        print("[1] 간편결제")
        print("[2] 카드 결제")

        choice = input("\n선택하세요: ")

        # -------------------------------
        # 간편결제
        # -------------------------------
        if choice == "1":

            print("\n📷 결제 QR을 스캔해주세요...")

            payment_barcode = scan_product.scan_barcode()

            # QR 인식 실패
            if payment_barcode is None:

                print("\n❌ QR 인식 실패")
                continue

            pay_type_name = detect_payment_type(
                payment_barcode
            )

            success = simple_payment.process_simple_payment(
                pay_type_name,
                final_price
            )

            if success:
                break

        # -------------------------------
        # 카드 결제
        # -------------------------------
        elif choice == "2":

            print("\n💳 카드 결제 완료!")
            break

        else:

            print("\n❌ 잘못된 입력입니다.")