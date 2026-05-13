import pay_balance
# ==========================================
# 간편결제 처리
# ==========================================
def process_simple_payment(
    pay_type_name,
    final_price
):

    user_balance = pay_balance.get_pay_balance(
        pay_type_name
    )

    print(
        f"\n💰 [{pay_type_name}] 잔액:"
        f" {user_balance:,}원"
    )

    # 잔액 충분
    if user_balance >= final_price:

        print("✅ 간편결제 승인 완료")

        return True

    # 잔액 부족
    else:

        lack_money = (
            final_price - user_balance
        )

        print("\n❌ 잔액 부족")

        print(
            f"💸 부족 금액:"
            f" {lack_money:,}원"
        )

        print(
            "\n↩ 결제 선택 화면으로 돌아갑니다..."
        )

        return False

