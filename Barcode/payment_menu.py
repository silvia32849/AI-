import simple_payment

# ==========================================
# 결제 선택 화면
# ==========================================
def payment_menu(
    is_simple_pay,
    pay_type_name,
    final_price
):

    while True:

        print("\n=== 결제 수단 선택 ===")

       
        print("[1] 간편결제")

        print("[2] 카드 결제")

        choice = input("\n선택하세요: ")

        # -------------------------------
        # 간편결제
        # -------------------------------
        if choice == "1":

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

            print("\n💳 카드 결제 준비 중입니다...")
            return

        else:

            print("\n❌ 잘못된 입력입니다.")