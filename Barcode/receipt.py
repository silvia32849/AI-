# ==========================================
# 영수증 출력
# ==========================================
def print_receipt(
    partner_name,
    pay_type_name,
    original_price,
    p_discount_amt,
    telecom,
    t_discount_amt,
    final_price
):

    print("\n" + "=" * 35)

    print(f"✅ 스캔 확인: {partner_name}")
    print(f"📢 결제 모드: {pay_type_name}")

    print("-" * 35)

    print(f"💵 판매 가격: {original_price:,}원")

    if p_discount_amt > 0:

        print(
            f"🎉 제휴사 할인: -{p_discount_amt:,}원"
        )

    if t_discount_amt > 0:

        print(
            f"🎉 통신사({telecom}) 할인:"
            f" -{t_discount_amt:,}원"
        )

    print("-" * 35)

    print(
        f"👉 최종 결제 금액:"
        f" {final_price:,}원"
    )

    print("=" * 35)

