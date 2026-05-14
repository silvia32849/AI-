# ==========================================
# 가격 계산
# ==========================================
def calculate_price(
    original_price,
    partner_discount,
    telecom_discount
):

    p_discount_amt = 0

    t_discount_amt = int(
        original_price * (telecom_discount / 100)
    )

    final_price = (
        original_price
        - t_discount_amt
    )

    return (
        p_discount_amt,
        t_discount_amt,
        final_price
    )