from pay_balance import get_pay_balance
# ==========================================
# 가격 계산
# ==========================================
def calculate_price(
    original_price,
    partner_name,
    partner_discount,
    telecom_discount
):

   # 제휴 할인 금액
    p_discount_amt = int(
        original_price * (partner_discount / 100)
    )

    # 제휴 할인 적용 가격
    discounted_price = (
        original_price - p_discount_amt
    )

    # 통신사 할인 금액
    t_discount_amt = int(
        discounted_price * (telecom_discount / 100)
    )

    # 할인 적용 후 금액
    total_price = (
        discounted_price - t_discount_amt
    )

    # 간편결제 잔액 조회
    balance = get_pay_balance(partner_name)

    # 잔액 차감
    if balance >= total_price:
        final_price = 0
    else:
        final_price = total_price - balance

    return (
        p_discount_amt,
        t_discount_amt,
        final_price
    )