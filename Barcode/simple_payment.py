# ==========================================
# 간편결제 처리
# ==========================================
def process_simple_payment(
    pay_type_name,
    final_price
):

    print("\n===================================")

    print(f"✅ {pay_type_name} 결제 진행")

    print(f"💰 결제 금액: {final_price:,}원")

    print("🎉 결제가 완료되었습니다!")

    print("===================================")

    return True